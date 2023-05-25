from django.shortcuts import render
from django.contrib import messages
import psycopg2
import locale
import uuid
from utils.query import *
from django.views.decorators.csrf import csrf_exempt
from manager import views as manager_views
locale.setlocale(locale.LC_ALL, '')
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

@csrf_exempt
def panitia_home(request):
    context = {}
    username = request.session['username']
    
    panitia = query(f"""
                    SELECT np.nama_depan, np.nama_belakang, np.nomor_hp, np.email, np.alamat, string_agg(DISTINCT nps.status, ', ') as status, p.jabatan, r.datetime
                    FROM panitia p
                    JOIN non_pemain np ON p.id_panitia = np.id
                    LEFT JOIN status_non_pemain nps ON np.id = nps.id_non_pemain
                    LEFT JOIN rapat r ON p.id_panitia = r.perwakilan_panitia
                    WHERE p.username = '{username}'
                    GROUP BY 1, 2, 3, 4, 5, 7, 8""")
    context = {
        'data_panitia' : panitia
    }
    return render(request, 'panitia_home.html', context=context)

def show_homelist(request):
    return render(request, "homelist.html")

def show_addpertandingan(request):
    return render(request, "addpertandingan.html")

def show_liststadium(request):
    return render(request, "liststadium.html")

def show_buatpertandingan(request):
    return render(request, "buatpertandingan.html")

# untuk rapat
def show_rapat(request, id_pertandingan):
    if request.method == 'GET':

            pertandingan = query("""SELECT r.id_pertandingan, string_agg(nama_tim, ' vs ') as tim_bertanding, s.nama, datetime
                                FROM rapat r, pertandingan p, tim_pertandingan tp, stadium s 
                                WHERE r.id_pertandingan = p.id_pertandingan AND p.id_pertandingan = tp.id_pertandingan AND p.stadium = s.id_stadium AND r.id_pertandingan = '{}'
                                GROUP BY r.id_pertandingan, stadium, s.nama, datetime;""".format(id_pertandingan))
                
            print(pertandingan)
            context = {'pertandingan': pertandingan}

            return render(request, 'rapat.html', context)

    if request.method == 'POST':
        isi_rapat = request.POST.get("rapat")
        
        query(f"""UPDATE RAPAT 
            SET isi_rapat = '{isi_rapat}'
            WHERE id_pertandingan = '{id_pertandingan}'""")
        
        return HttpResponseRedirect(reverse('panitia:show_pertandingan'))
    
    return render(request, 'rapat.html')

def mulai_pertandingan(request):
    context = {}
    
    username = request.session['username']
    
    tim1_info = query(f"""
                     SELECT distinct t.nama_tim
                        FROM pemain pm, peristiwa pr, pertandingan p, tim_pertandingan tp, tim t, rapat r, panitia pa, tim_manajer tm
                        WHERE pr.id_pemain = pm.id_pemain AND pr.id_pertandingan = p.id_pertandingan
                        AND p.id_pertandingan = tp.id_pertandingan AND tp.nama_tim = t.nama_tim
                        AND tm.nama_tim = t.nama_tim AND tm.id_manajer = r.manajer_tim_a
                        AND r.perwakilan_panitia = pa.id_panitia AND pa.username = '{username}'
                        GROUP BY 1""")
    
    tim2_info = query(f"""
                       SELECT distinct t.nama_tim
                        FROM pemain pm, peristiwa pr, pertandingan p, tim_pertandingan tp, tim t, rapat r, panitia pa, tim_manajer tm
                        WHERE pr.id_pemain = pm.id_pemain AND pr.id_pertandingan = p.id_pertandingan
                        AND p.id_pertandingan = tp.id_pertandingan AND tp.nama_tim = t.nama_tim
                        AND tm.nama_tim = t.nama_tim AND tm.id_manajer = r.manajer_tim_a
                        AND r.perwakilan_panitia = pa.id_panitia AND pa.username = '{username}'
                        GROUP BY 1""")
    
    context = {
        'tim1_info' : tim1_info,
        'tim2_info' : tim2_info
    }
    
    return render(request, "mulaipertandingan.html", context=context)
    
    
    
    return render(request, "mulaipertandingan.html")

def pilih_peristiwa(request):
    return render(request, "pilihperistiwa.html")

def show_incomplete(request):
    return render(request, "incomplete.html")

def show_listperistiwa(request, nama_tim):
    context = {}
    
    username = request.session['username']
    
    nama_pemain_A = query(f"""
                        SELECT distinct pm.nama_depan, pm.nama_belakang, t.nama_tim
                        FROM pemain pm, peristiwa pr, pertandingan p, tim_pertandingan tp, tim t, rapat r, panitia pa, tim_manajer tm
                        WHERE pr.id_pemain = pm.id_pemain AND pr.id_pertandingan = p.id_pertandingan
                        AND p.id_pertandingan = tp.id_pertandingan AND tp.nama_tim = t.nama_tim
                        AND tm.nama_tim = t.nama_tim AND tm.id_manajer = r.manajer_tim_a
                        AND r.perwakilan_panitia = pa.id_panitia AND pa.username = '{username}'
                        GROUP BY 1, 2, 3""".format(nama_tim))
    
    peristiwa_A = query(f"""
                        SELECT distinct pr.jenis
                        FROM pemain pm, peristiwa pr, pertandingan p, tim_pertandingan tp, tim t, rapat r, panitia pa, tim_manajer tm
                        WHERE pr.id_pemain = pm.id_pemain AND pr.id_pertandingan = p.id_pertandingan
                        AND p.id_pertandingan = tp.id_pertandingan AND tp.nama_tim = t.nama_tim
                        AND tm.nama_tim = t.nama_tim AND tm.id_manajer = r.manajer_tim_a
                        AND r.perwakilan_panitia = pa.id_panitia AND pa.username = '{username}'
                        GROUP BY 1""".format(nama_tim))
    
    nama_pemain_B = query(f"""
                        SELECT distinct pm.nama_depan, pm.nama_belakang, t.nama_tim
                        FROM pemain pm, peristiwa pr, pertandingan p, tim_pertandingan tp, tim t, rapat r, panitia pa, tim_manajer tm
                        WHERE pr.id_pemain = pm.id_pemain AND pr.id_pertandingan = p.id_pertandingan
                        AND p.id_pertandingan = tp.id_pertandingan AND tp.nama_tim = t.nama_tim
                        AND tm.nama_tim = t.nama_tim AND tm.id_manajer = r.manajer_tim_b
                        AND r.perwakilan_panitia = pa.id_panitia AND pa.username = '{username}'
                        GROUP BY 1, 2, 3""".format(nama_tim))
    
    peristiwa_B = query(f"""
                        SELECT distinct pr.jenis
                        FROM pemain pm, peristiwa pr, pertandingan p, tim_pertandingan tp, tim t, rapat r, panitia pa, tim_manajer tm
                        WHERE pr.id_pemain = pm.id_pemain AND pr.id_pertandingan = p.id_pertandingan
                        AND p.id_pertandingan = tp.id_pertandingan AND tp.nama_tim = t.nama_tim
                        AND tm.nama_tim = t.nama_tim AND tm.id_manajer = r.manajer_tim_b
                        AND r.perwakilan_panitia = pa.id_panitia AND pa.username = '{username}'
                        GROUP BY 1""".format(nama_tim))
    
    
    context = {
        'nama_pemainA' : nama_pemain_A,
        'peristiwaA' : peristiwa_A,
        'nama_pemainB' : nama_pemain_B,
        'peristiwaB' : peristiwa_B
        
    }
    
    return render(request, "listperistiwa.html", context=context)

@csrf_exempt
def show_tablelist(request):
    context = {}
    
    username = request.session['username']
    
    tim1_query = query(f"""
                        SELECT t.nama_tim, p.start_datetime, tp.skor
                        FROM pertandingan p
                        JOIN tim_pertandingan tp ON p.id_pertandingan = tp.id_pertandingan
                        JOIN tim t ON tp.nama_tim = t.nama_tim
                        LEFT JOIN tim_manajer tm ON t.nama_tim = tm.nama_tim
                        LEFT JOIN rapat r ON tm.id_manajer = r.manajer_tim_a
                        LEFT JOIN panitia pa ON r.perwakilan_panitia = pa.id_panitia
                        WHERE pa.username = '{username}'
                        GROUP BY 1, 2, 3""")
    
    tim2_query = query(f"""
                        SELECT t.nama_tim, p.start_datetime , tp.skor
                        FROM pertandingan p
                        JOIN tim_pertandingan tp ON p.id_pertandingan = tp.id_pertandingan
                        JOIN tim t ON tp.nama_tim = t.nama_tim
                        LEFT JOIN tim_manajer tm ON t.nama_tim = tm.nama_tim
                        LEFT JOIN rapat r ON tm.id_manajer = r.manajer_tim_b
                        LEFT JOIN panitia pa ON r.perwakilan_panitia = pa.id_panitia
                        WHERE pa.username = '{username}'
                        GROUP BY 1, 2, 3""")
    
    nama_tim1 = tim1_query[0]['nama_tim']
    nama_tim2 = tim2_query[0]['nama_tim']
    
    skor_tim1 = tim1_query[0]['skor']
    skor_tim2 = tim2_query[0]['skor']
    
    pemenang_query = query(f"""
                           SELECT 
                           CASE 
                           WHEN CAST('{skor_tim1}' AS INTEGER) > CAST('{skor_tim2}' AS INTEGER) THEN '{nama_tim1}'
                           WHEN CAST('{skor_tim1}' AS INTEGER) < CAST('{skor_tim2}' AS INTEGER) THEN '{nama_tim2}'
                           END AS pemenang
                           FROM tim_pertandingan tp
                           JOIN pertandingan p ON tp.id_pertandingan = p.id_pertandingan
                           JOIN rapat r ON p.id_pertandingan = r.id_pertandingan
                           JOIN panitia pa ON r.perwakilan_panitia = pa.id_panitia
                           WHERE pa.username = '{username}'
                           GROUP BY 1""")
    
                               
    time_pertandingan = query(f"""
                                    SELECT p.start_datetime
                                    FROM pertandingan p
                                    JOIN tim_pertandingan tp ON p.id_pertandingan = tp.id_pertandingan
                                    JOIN tim t ON tp.nama_tim = t.nama_tim
                                    LEFT JOIN tim_manajer tm ON t.nama_tim = tm.nama_tim
                                    LEFT JOIN rapat r ON p.id_pertandingan = r.id_pertandingan
                                    LEFT JOIN panitia pa ON r.perwakilan_panitia = pa.id_panitia
                                    WHERE pa.username = '{username}'
                                    GROUP BY 1""")
                                    
    
    context = {
        'tim1' : tim1_query,
        'tim2' : tim2_query,
        'pemenang' : pemenang_query,
        'waktu' : time_pertandingan
    }
    
    return render(request, "tablelist.html", context=context)

def show_finished(request):
    return render(request, "finished.html")

def show_pertandingan(request):
    if request.method == 'GET':

            pertandingan = query("""SELECT r.id_pertandingan, string_agg(nama_tim, ' vs ') as tim_bertanding, s.nama, datetime
                                FROM rapat r, pertandingan p, tim_pertandingan tp, stadium s 
                                WHERE r.id_pertandingan = p.id_pertandingan AND p.id_pertandingan = tp.id_pertandingan AND p.stadium = s.id_stadium 
                                GROUP BY r.id_pertandingan, stadium, s.nama, datetime;""")
                
            print(pertandingan)
            context = {'pertandingan': pertandingan}

            return render(request, 'pilihpertandingan.html', context)
 
@csrf_exempt
def kelola_pertandingan(request):
    username = request.session['username']
    
    list_pertandingan = query(f"""
                              SELECT p.id_pertandingan, tp.nama_tim
                                FROM pertandingan p
                                JOIN tim_pertandingan tp ON p.id_pertandingan = tp.id_pertandingan
                                JOIN tim t ON tp.nama_tim = t.nama_tim
                                LEFT JOIN rapat r ON p.id_pertandingan = r.id_pertandingan
                                LEFT JOIN panitia pa ON r.perwakilan_panitia = pa.id_panitia
                                WHERE pa.username = '{username}'
                                GROUP BY 1, 2""")
                                
    print("try")
    print("list_pertandingan:", list_pertandingan)
    print("length of list_pertandingan:", len(list_pertandingan))
    
    if len(list_pertandingan) == 0:
        print("belum ada pertandingan")
        return HttpResponseRedirect(reverse('panitia:show_incomplete'))
    
    print("nama_tim:", list_pertandingan[0]['nama_tim'])
    return HttpResponseRedirect(reverse('panitia:show_tablelist'))

