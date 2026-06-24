def custom_fence(fence: str = "+"):
    def add_fence(func):
        def wrapper(text: str):
            print(fence * len(text))
            func(text)
            print(fence * len(text))
        return wrapper
    return add_fence

@custom_fence(fence="*")
def greet(name:str):
    print(f"Hello, {name}!")
    
greet("David")

##Ejercicio 2 

def redondear(precision: int):
    def func_decorator(func):
        def logic(*args, **kwargs)-> float:
            resultado = func(*args, **kwargs) ##convierte los parametros en una tupla y un diccionario 
            return round(resultado, precision)
        return logic
    return func_decorator

@redondear(precision=3)
def calcular_pi() -> float:
    return 3.14159265

@redondear(precision=1)
def calcular_iva(precio: float) -> float:
    return precio * 0.19

# Pruebas
print(calcular_pi())        # Debe mostrar: 3.142
print(calcular_iva(100))    # Debe mostrar: 19.0