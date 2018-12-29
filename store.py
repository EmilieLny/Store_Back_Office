from bottle import run, template, static_file, get, post, delete, request, error, response
import os
import json
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='mysqlEmi',
                             db='STORE',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


@get("/")
def index():
    return template("index.html")


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


####### CATEGORY #######

@post("/category")
def add_category():
    try:
        with connection.cursor() as cursor:
            newCatName = request.forms.get("name")
            if len(newCatName) == 0:
                return json.dumps({"STATUS": "ERROR", "MSG": "Input not accepted"})
            sql = "INSERT INTO CATEGORIES (name) VALUES('{}')".format(newCatName)
            cursor.execute(sql)
            connection.commit()
            catId = cursor.lastrowid
            return json.dumps({"STATUS": "SUCCESS", "CAT_ID": catId})
    except Exception as e:
        if response.status_code == 400:
            return json.dumps({"STATUS": "ERROR", "MSG": "Bad request"})
        elif response.status_code == 500:
            return json.dumps({"STATUS": "ERROR", "MSG": "Internal error"})
        elif response.status_code == 200:
            return json.dumps({"STATUS": "ERROR", "MSG": "Category already exists"})
        else:
            return json.dumps({"STATUS": "ERROR", "MSG": "ERROR : " + str(e)})


@delete("/category/<catId>")
def remove_category(catId):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM CATEGORIES WHERE id={}".format(catId)
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "MSG": "Category deleted successfully"}) #201
    except Exception as e:
        if response.status_code == 404:
            return json.dumps({"STATUS": "ERROR", "MSG": "Category not found"})
        else:
            return json.dumps({"STATUS": "ERROR", "MSG": "ERROR : " + str(e)})

@get('/categories')
def categories():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM CATEGORIES;"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "MSG": "Categories fetched", 'CATEGORIES': result})
    except Exception as e:
        if response.status_code == 500:
            return json.dumps({"STATUS": "ERROR", "MSG": 'Internal error 500'})
        else:
            return json.dumps({"STATUS": "ERROR", "MSG": "ERROR : " + str(e)})



####### PRODUCT #######

@post("/product")
def add_product():
    try:
        with connection.cursor() as cursor:
            catChoosed = request.forms.get("category")
            titlePdt = request.forms.get("title")
            descPdt = request.forms.get("desc")
            favPdt = request.forms.get("favorite")
            if favPdt == 'on':
                favPdt = True
            else:
                favPdt = False
            pricePdt = request.forms.get("price")
            imgPdt = request.forms.get("img_url")
            sql1 = "INSERT INTO PRODUCTS (title, desc_pdt, favorite, price, img_url, category) "
            sql2 = "VALUES('{}', '{}', {}, '{}', '{}', {})".format(titlePdt, descPdt, favPdt, pricePdt, imgPdt,
                                                                   catChoosed)
            cursor.execute(sql1 + sql2)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "MSG": "The product was added successfully !"})
    except:
        try:
            with connection.cursor() as cursor:
                catChoosed = request.forms.get("category")
                titlePdt = request.forms.get("title")
                descPdt = request.forms.get("desc")
                favPdt = request.forms.get("favorite")
                if favPdt == 'on':
                    favPdt = True
                else:
                    favPdt = False
                pricePdt = request.forms.get("price")
                imgPdt = request.forms.get("img_url")
                sql1 = "UPDATE PRODUCTS SET "
                sql2 = "desc_pdt='{}', favorite={}, price='{}', img_url='{}', category={} WHERE title='{}'".format(descPdt,
                                                                                                               favPdt,
                                                                                                               pricePdt,
                                                                                                               imgPdt,
                                                                                                               catChoosed,
                                                                                                                titlePdt)
                cursor.execute(sql1 + sql2)
                connection.commit()
                return json.dumps({"STATUS": "SUCCESS", "MSG": "The product was updated successfully !"})
        except Exception as e:
            return json.dumps(
                {"STATUS": "ERROR", "MSG": "The product was not created/updated due to an error : " + str(e)})


@get("/product/<id>")
def product(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM PRODUCTS WHERE id={}".format(id)
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "MSG": 'The product was fetched successfully !', 'PRODUCT': result})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": 'The product was not fetched due to an error :' + str(e)})


@delete("/product/<id>")
def remove_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM PRODUCTS WHERE id={}".format(id)
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS", "MSG": "The product was deleted successfully !"})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": "The product was not deleted due to an error : " + str(e)})


@get('/products')
def products():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM PRODUCTS;"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "MSG": "Products fetched", 'PRODUCTS': result})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": "Internal error : " + str(e)})


@get('/category/<id>/products')
def products_by_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM PRODUCTS WHERE category = {};".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({"STATUS": "SUCCESS", "MSG": "Products fetched", "PRODUCTS": result})
    except Exception as e:
        return json.dumps({"STATUS": "ERROR", "MSG": "Internal error : " + str(e)})


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


@error(404)
def error404(error):
    return template("<h1>You get lost ? 404 Error..</h1>")


run(host='0.0.0.0', port=os.environ.get('PORT', 7000))
