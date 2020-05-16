from cliente import Cliente
from producto import Producto
import os

dirname = os.path.dirname(__file__)


def listar_clientes(imprimir):

    filename = os.path.join(dirname, 'db/clientes.txt')

    data_clientes = open(filename, 'r')

    lista_clientes = {}

    for dc in data_clientes:
        linea = [x.strip() for x in dc.split(';')]
        if len(linea[0]) > 0:
            cliente = Cliente(linea[0], linea[1], linea[2], linea[3])
            lista_clientes[linea[0]] = cliente
    data_clientes.close()

    if imprimir:
        for cli in lista_clientes.items():
            print('Cliente: '+cli[1].nombre + ' ' + cli[1].apellido + ' Codigo: ' + cli[1].codigo)
    else:
        return lista_clientes


def listar_productos(imprimir):

    filename = os.path.join(dirname, 'db/productos.txt')

    data_productos = open(filename, 'r')

    lista_productos = {}

    for dp in data_productos:
        linea = [x.strip() for x in dp.split(';')]
        if len(linea[0]) > 0:
            producto = Producto(linea[0], linea[1], linea[2], linea[3])
            lista_productos[linea[0]] = producto
    data_productos.close()

    if imprimir:
        for pro in lista_productos.items():
            print('Articulo: ' + pro[1].nombre + ' Cantidad: ' + pro[1].cantidad
                  + ' Valor: ' + pro[1].valor)
    else:
        return lista_productos


def asociar_productos():

    lista_detalle = {}

    clientes = listar_clientes(False)

    productos = listar_productos(False)

    producto, cantidad = None, None

    filename = os.path.join(dirname, 'db/clientes_productos.txt')

    data_detalle = open(filename, 'r')

    for dt in data_detalle:
        linea = [x.strip() for x in dt.split(';')]
        if len(linea[0]) > 0:
            if linea[0] not in lista_detalle:
                lista_detalle[linea[0]] = {'cliente': clientes.get(linea[0]), 'compras': []}

                if linea[1].startswith('P'):
                    producto = productos[linea[1]]
                else:
                    cantidad = linea[1]

                if linea[2].startswith('P'):
                    producto = productos[linea[2]]
                else:
                    cantidad = linea[2]

                lista_detalle[linea[0]]['compras'].append({'producto': producto, 'cantidad': cantidad})
            else:

                if linea[1].startswith('P'):
                    producto = productos[linea[1]]
                else:
                    cantidad = linea[1]

                if linea[2].startswith('P'):
                    producto = productos[linea[2]]
                else:
                    cantidad = linea[2]

                lista_detalle[linea[0]]['compras'].append({'producto': producto, 'cantidad': cantidad})

    return lista_detalle


def calcular_ventas_clientes(cliente):

    lista_detalle = asociar_productos()

    if len(cliente) > 0:
        seleccionado = lista_detalle.get(cliente)
        print('Cliente: '+seleccionado.get('cliente').nombre + ' ' + seleccionado.get('cliente').apellido + ' Codigo: '
              + seleccionado.get('cliente').codigo)
        print("///////////////////////// Compras ///////////////")
        valor_total = 0
        for co in seleccionado.get('compras'):
            valor = (float(co.get('producto').valor) * float(co.get('cantidad')))
            valor_total += valor
            print('Articulo: ' + co.get('producto').nombre + ' Cantidad: ' + co.get('cantidad')
                  + ' Valor: ' + str(valor))
        print('Valor total: ' + str(valor_total))
    else:
        for ld in lista_detalle.items():
            cliente = ld[1].get('cliente')
            print("===========================")
            print('Cliente: '+cliente.nombre + ' ' + cliente.apellido + ' Codigo: ' + cliente.codigo)
            print("///////////////////////// Compras ///////////////")
            valor_total = 0
            for co in ld[1].get('compras'):
                valor = (float(co.get('producto').valor) * float(co.get('cantidad')))
                valor_total += valor
                print('Articulo: ' + co.get('producto').nombre + ' Cantidad: ' + co.get('cantidad')
                      + ' Valor: ' + str(valor))
            print('Valor total: ' + str(valor_total))


def inventario_productos():
    lista_detalle = asociar_productos()
    all_productos = listar_productos(False)

    for p in all_productos.items():
        cantidad = int(p[1].cantidad)
        for ld in lista_detalle.items():
            for co in ld[1].get('compras'):
                if co.get('producto').nombre == p[1].nombre:
                    cantidad -= int(co.get('cantidad'))
        print('Articulo: ' + p[1].nombre + ' Cantidad: ' + str(cantidad))


def iniciar_programa():
    print("========== Menu =========")
    print("1) Listar Clientes")
    print("2) Listar Productos")
    print("3) Inventario de productos")
    print("4) Ventas x Clientes")
    print("5) Busqueda de venta por clientes")
    opcion = input()

    if opcion == '1':
        listar_clientes(True)
    elif opcion == '2':
        listar_productos(True)
    elif opcion == '3':
        inventario_productos()
    elif opcion == '4':
        calcular_ventas_clientes('')
    else:
        print("Ingrese codigo del cliente: ")
        codigo_cliente = input()
        calcular_ventas_clientes(codigo_cliente)


iniciar_programa()
