from django.shortcuts import render
from django.contrib import messages
import psycopg2
import locale
import uuid
locale.setlocale(locale.LC_ALL, '')

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

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
        ORDER BY Nama_Pemain ASC;
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
            group by 1, 2
            ORDER BY Nama_Pelatih ASC;;
            """)
    pelatih_tersedia_list = cursor.fetchall()

    context = {
        'pelatih_tersedia_list' : pelatih_tersedia_list
        }
    
    db_connection.close()
    return render(request, "addpelatih.html", context=context)

def add_player(request):
    context = {}
    db_connection = psycopg2.connect(
        host="localhost",
        database="fauziah.putri11",
        port="5433",
        user="postgres",
        password="putisql123"
    )
    cursor = db_connection.cursor()
    if request.method == 'POST':
        id_player = request.POST.get("player")    
        cursor.execute("set search_path to uleague")
        query_add = "UPDATE PEMAIN SET Nama_Tim = %s WHERE ID_Pemain = %s"

        try:
            cursor.execute(query_add, ("Manchester United", id_player))
            print(cursor)
            db_connection.commit()

        except Exception as e:
            messages.error(request, e)
            print('ERROR NIH')
            db_connection.rollback()

    db_connection.close()
    return HttpResponseRedirect(reverse('manager:show_teamdetail'))

def add_coach(request):
    context = {}
    db_connection = psycopg2.connect(
        host="localhost",
        database="fauziah.putri11",
        port="5433",
        user="postgres",
        password="putisql123"
    )
    cursor = db_connection.cursor()
    if request.method == 'POST':
        id_coach = request.POST.get("coach")    
        cursor.execute("set search_path to uleague")
        query_add = "UPDATE PELATIH SET Nama_Tim = %s WHERE ID_Pelatih = %s"

        try:
            cursor.execute(query_add, ("Manchester United", id_coach))
            print(cursor)
            db_connection.commit()

        except Exception as e:
            messages.error(request, e)
            print('ERROR NIH')
            db_connection.rollback()

    db_connection.close()
    return HttpResponseRedirect(reverse('manager:show_teamdetail'))

def get_pemain(nama_tim, cursor):
    query_get_pemain = """
    SELECT Pm.ID_Pemain, CONCAT(Pm.Nama_Depan, ' ', Pm.Nama_Belakang) as Nama_Pemain, Nomor_HP, Tgl_Lahir, Is_Captain, Posisi, NPM, Jenjang 
    FROM PEMAIN Pm WHERE Pm.Nama_Tim = %s
    """
    pemain_list = cursor.execute(query_get_pemain, (nama_tim,))
    pemain_list = cursor.fetchall()
    # print(pemain_list)
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
    return pelatih_list

def make_captain(request):
    context = {}
    db_connection = psycopg2.connect(
        host="localhost",
        database="fauziah.putri11",
        port="5433",
        user="postgres",
        password="putisql123"
    )
    cursor = db_connection.cursor()

    query_update_captain = """
    UPDATE PEMAIN
            SET Is_Captain = 'TRUE'
            WHERE Nama_Tim = %s
            and ID_Pemain = %s
    """

    if request.method == 'POST':
        id_new_captain = request.POST.get("capt")    
        cursor.execute("set search_path to uleague")
        cursor.execute(query_update_captain, ("Manchester United", id_new_captain))
        print(cursor)
    db_connection.commit()
    db_connection.close()
    return HttpResponseRedirect(reverse('manager:show_teamdetail'))


def delete_pemain(request):
    context = {}
    db_connection = psycopg2.connect(
        host="localhost",
        database="fauziah.putri11",
        port="5433",
        user="postgres",
        password="putisql123"
    )
    cursor = db_connection.cursor()
    
    query_delete_player = """
    UPDATE PEMAIN
        SET Nama_Tim = NULL
        WHERE ID_Pemain = %s
    """

    if request.method == 'POST':
        id_player = request.POST.get("player")    
        cursor.execute("set search_path to uleague")
        cursor.execute(query_delete_player, (id_player,))
        print(cursor)

    db_connection.commit()
    db_connection.close()
    return HttpResponseRedirect(reverse('manager:show_teamdetail'))

def delete_pelatih(request):
    context = {}
    db_connection = psycopg2.connect(
        host="localhost",
        database="fauziah.putri11",
        port="5433",
        user="postgres",
        password="putisql123"
    )
    cursor = db_connection.cursor()
    
    query_delete_coach = """
    UPDATE PELATIH
        SET Nama_Tim = NULL
        WHERE ID_Pelatih = %s
    """

    if request.method == 'POST':
        id_coach = request.POST.get("coach")
        # print(request.POST) 
        print(id_coach)    

        cursor.execute("set search_path to uleague")
        cursor.execute(query_delete_coach, (id_coach,))
        print(cursor)

    db_connection.commit()
    db_connection.close()
    return HttpResponseRedirect(reverse('manager:show_teamdetail'))