from django.shortcuts import render
from django.contrib import messages
import psycopg2
import locale
import uuid
locale.setlocale(locale.LC_ALL, '')

def manager_home(request):
    return render(request, 'manager_home.html')

def show_timregist(request):
    return render(request, "teamregist.html")

def show_teamdetail(request):
    context = {}
    db_connection = psycopg2.connect(
        host="localhost",
        database="fauziah.putri11",
        port="5433",
        user="postgres",
        password="putisql123"
    )
    cursor = db_connection.cursor()
    
    cursor.execute("set search_path to uleague")
    context = {
        'pemain_list' : get_pemain("Manchester United", cursor),
        'pelatih_list' : get_pelatih("Manchester United", cursor)
        }
    db_connection.close()
    return render(request, "teamdetail.html", context=context)

def show_addpemain(request):
    context = {}
    db_connection = psycopg2.connect(
        host="localhost",
        database="fauziah.putri11",
        port="5433",
        user="postgres",
        password="putisql123"
    )
    cursor = db_connection.cursor()
    
    cursor.execute("set search_path to uleague")
    pemain_tersedia_list = cursor.execute("""
        SELECT ID_Pemain, CONCAT(Nama_Depan, ' ', Nama_Belakang) as Nama_Pemain, Posisi
        FROM Pemain
        WHERE Nama_Tim is NULL
        """)
    pemain_tersedia_list = cursor.fetchall()

    context = {
        'pemain_tersedia_list' : pemain_tersedia_list
        }
    print(context)
    db_connection.close()
    return render(request, "addpemain.html", context=context)

def show_addpelatih(request):
    context = {}
    db_connection = psycopg2.connect(
        host="localhost",
        database="fauziah.putri11",
        port="5433",
        user="postgres",
        password="putisql123"
    )
    cursor = db_connection.cursor()
    
    cursor.execute("set search_path to uleague")
    pelatih_tersedia_list = cursor.execute( """
            SELECT Pl.ID_Pelatih, CONCAT(Nama_Depan, ' ', Nama_Belakang) as Nama_Pelatih, string_agg(Spesialisasi, ', ') as Jenis_Spesialisasi
            FROM Non_Pemain Np, Pelatih Pl, Spesialisasi_Pelatih Sp
            WHERE Np.ID = Pl.ID_Pelatih
            and Pl.ID_Pelatih = Sp.ID_Pelatih
            and Pl.Nama_Tim is NULL
            group by 1, 2;
            """)
    pelatih_tersedia_list = cursor.fetchall()

    context = {
        'pelatih_tersedia_list' : pelatih_tersedia_list
        }
    
    db_connection.close()
    return render(request, "addpelatih.html", context=context)

def get_pemain(nama_tim, cursor):
    query_get_pemain = """
    SELECT Pm.ID_Pemain, CONCAT(Pm.Nama_Depan, ' ', Pm.Nama_Belakang) as Nama_Pemain, Nomor_HP, Tgl_Lahir, Is_Captain, Posisi, NPM, Jenjang 
    FROM PEMAIN Pm WHERE Pm.Nama_Tim = %s
    """
    pemain_list = cursor.execute(query_get_pemain, (nama_tim,))
    pemain_list = cursor.fetchall()
    print(pemain_list)
    return pemain_list

def get_pelatih(nama_tim, cursor):
    query_get_pelatih = """
    SELECT Pl.ID_Pelatih, CONCAT(Nama_Depan, ' ', Nama_Belakang) as Nama_Pelatih, Nomor_HP, Email, Alamat, Spesialisasi 
    FROM Non_Pemain Np, Pelatih Pl, Spesialisasi_Pelatih Sp 
    WHERE Np.ID = Pl.ID_Pelatih
    and Pl.ID_Pelatih = Sp.ID_Pelatih
    and Pl.Nama_Tim = %s
    """
    pelatih_list = cursor.execute(query_get_pelatih, (nama_tim,))
    pelatih_list = cursor.fetchall()
    print(pelatih_list)
    return pelatih_list