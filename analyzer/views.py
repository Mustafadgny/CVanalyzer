from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import PyPDF2
import google.genai as genai
from django.conf import settings

from .forms import CvUploadForm
from .models import UploadedCv

import os
from django.http import JsonResponse, FileResponse

from pdf2image import convert_from_path

from PIL import ImageDraw


# === 📤 CV Yükleme ===


def upload_cv(request):
    preview_url = None
    if request.method == 'POST':
        form = CvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.user = None
            cv.save()
            return redirect('cv_list')

            # 📌 PDF'i görsele çevir
            pdf_path = cv.pdf.path
            output_dir = os.path.join(settings.MEDIA_ROOT, "previews")
            os.makedirs(output_dir, exist_ok=True)
            images = convert_from_path(pdf_path, dpi=150, poppler_path=r"C:\Users\mustafa\Downloads\poppler-24.08.0\poppler-24.08.0\Library\bin")
            if images:
                preview_path = os.path.join(output_dir, f"{cv.id}_preview.png")
                images[0].save(preview_path, "PNG")
                preview_url = settings.MEDIA_URL + "previews/" + f"{cv.id}_preview.png"

            return render(request, 'dashboard.html', {
                'form': CvUploadForm(),
                'cvs': UploadedCv.objects.all(),
                'preview_url': preview_url
            })
    else:
        return render(request, 'dashboard.html', {
            'form': CvUploadForm(),
            'cvs': UploadedCv.objects.all()
        })


# === 📑 CV Listesi (artık dashboard'a yönlendirecek) ===
def cv_list(request):
    # Bu view eski /cvs/ adresinden geldiğinde dashboard'u döndürür
    return render(request, 'dashboard.html', {
        'form': CvUploadForm(),
        'cvs': UploadedCv.objects.all()
    })


def analyze_cv(request, cv_id):
    cv = get_object_or_404(UploadedCv, id=cv_id)
    pdf_path = cv.pdf.path
    text = ""
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

    # Gemini'ye özel analiz
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    prompt = f"""
    Aşağıdaki CV metnini incele.
    - Güçlü yönlerini kısaca maddeler halinde yaz (en fazla 3 madde).
    - Geliştirilmesi gereken yönlerini kısaca maddeler halinde yaz (en fazla 2 madde).
    - Türkçe cevapla, sade ve öz yaz.

    CV METNİ:
    {text}
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )
        ai_reply = response.text
        # sadece dolu satırları al
        findings = [line.strip() for line in ai_reply.split("\n") if line.strip()]
        return JsonResponse({"findings": findings})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
@csrf_exempt
def help_me(request):
    if request.method == 'POST':
        # === 📄 Son yüklenen CV'nin içeriğini oku ===
        last_cv = UploadedCv.objects.last()
        cv_content = ""

        if last_cv and last_cv.pdf:
            pdf_path = last_cv.pdf.path
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            cv_content += text

        # === Kullanıcı mesajı ===
        user_message = request.POST.get('message', '').strip()

        # === Geçmiş yoksa başlat ===
        if 'chat_history' not in request.session:
            request.session['chat_history'] = []
        chat_history = request.session['chat_history']

        # === 📋 Mevcut CV listesini ekle ===
        cvs = UploadedCv.objects.all()
        cv_names = [cv.pdf.name for cv in cvs]
        cv_context = "Yüklenmiş CV dosyaları: " + ", ".join(cv_names) if cv_names else "Henüz yüklenmiş CV yok."

        # === Gemini client ===
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        # === Gemini'ye gönderilecek içerikler ===
        contents = []

        # 1️⃣ CV dosya listesi bilgisi
        contents.append({
            "role": "user",
            "parts": [{"text": f"Bilgi: {cv_context}"}]
        })

        # 2️⃣ CV içeriğini de Gemini'ye verelim (varsa)
        if cv_content:
            contents.append({
                "role": "user",
                "parts": [{"text": f"İşte yüklenmiş CV'nin içeriği:\n{cv_content}\n--- Yukarıdaki CV içeriğini aklında tut ve değerlendirmelerde kullan."}]
            })

        # 3️⃣ Geçmiş mesajları ekle
        for item in chat_history:
            contents.append({"role": "user", "parts": [{"text": item['user']}]} )
            contents.append({"role": "model", "parts": [{"text": item['ai']}]})

        # 4️⃣ Yeni kullanıcı mesajını en sona ekle
        contents.append({"role": "user", "parts": [{"text": user_message}]})

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents
            )
            ai_reply = response.text

            # Geçmişe ekle
            chat_history.append({"user": user_message, "ai": ai_reply})
            request.session['chat_history'] = chat_history

            return JsonResponse({"reply": ai_reply})

        except Exception as e:
            return JsonResponse({"error": str(e)})

    # GET isteği için basit sayfa
    return render(request, 'help_me_chat.html')


# === 🏠 Dashboard ===
def dashboard(request):
    return render(request, 'dashboard.html', {
        'form': CvUploadForm(),
        'cvs': UploadedCv.objects.all()
    })


# === 🗑️ CV Sil ===
@csrf_exempt
def delete_cv(request, cv_id):
    if request.method == 'POST':
        cv = get_object_or_404(UploadedCv, id=cv_id)

        # önce fiziksel dosyayı sil
        if cv.pdf and os.path.isfile(cv.pdf.path):
            os.remove(cv.pdf.path)

        # sonra veritabanı kaydını sil
        cv.delete()

        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid request"}, status=400)


import fitz

@csrf_exempt
def analyze_image(request, cv_id):
    poppler_bin_path = r"C:\Users\mustafa\Downloads\poppler-24.08.0\poppler-24.08.0\Library\bin"
    cv = get_object_or_404(UploadedCv, id=cv_id)
    pdf_path = cv.pdf.path

    # Sadece ilk sayfanın görselini alalım, kutu çizmeden
    from pdf2image import convert_from_path

    images = convert_from_path(
        pdf_path,
        dpi=150,
        poppler_path=poppler_bin_path,
        first_page=1,
        last_page=1
    )
    if not images:
        return JsonResponse({"error": "PDF sayfası bulunamadı."}, status=400)

    img = images[0].convert("RGBA")

    # Kutucuk çizimini kaldırdık, doğrudan kaydediyoruz
    # Eğer çok büyükse yarı boyutuna küçültelim:
    w, h = img.size
    img = img.resize((w // 2, h // 2))

    # Kaydet
    output_dir = os.path.join(settings.MEDIA_ROOT, "analyzed")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{cv_id}_analyzed.png")
    img.save(output_path)

    return FileResponse(open(output_path, "rb"), content_type="image/png")