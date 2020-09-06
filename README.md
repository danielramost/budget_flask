## Simple budget app in Flask

The goal of this app is to show a list of expenses and being able to add and modify them. I also needed to be able to export the expenses list and then delete them all once exported.

This app is a tool to add expenses in an Excel file I use as a budget record, in which I have a sheet for incomes, another one for expenses, and another one to show my current balance.

I used Excel and Dropbox to add new expenses directly in my spreadsheet from my phone but it was too slow. Then I built this tool to add expenses from my cellphone and then export them on weekends to update my budget file.

### Backend server

All my data is stored in Firestore. The `config.py` script should be used to specify the `service_account.json` file to communicate with Firebase.

### Hosting

I used a bare-metal server configured according to this great guide: [https://youtu.be/goToXTC96Co](https://youtu.be/goToXTC96Co)

## Setup

### Spanish locale

On Ubuntu Server, add the es_CO locale:

```bash
locale -a # Check the locale currently supported
sudo locale-gen es_CO.utf8 # Add a new locale
sudo update-locale
```

### Config variables

Clone the repository and change the file `config.py` with the right values.

### Python packages

On a virtual environment:

```bash
pip install wheel
pip install -r requirements.txt
```

### Running the app

```bash
export FLASK_ENV=development
python run.py
```

## TODO

### Iteración actual

1. mejorar la seguridad. Esto requiere usar un secret_key y ese campo oculto para enviar forms por post. Agregar otras cosas que ameriten.
1. cambiar tabla por otro tipo de agrupador que sea responsive u ocultar campos de la tabla cuando se haga chiquita
1. mirar si se puede limitar el ancho del form en la vista de desktop
1. revisar todo el layout en general para que trabaje responsive
1. cambiar la lógica para entrar directo a crear. La función secundaria es la de consulta y descarga.
1. validar datos al guardar. Que algunos sean obligatorios y el formato.
1. función de eliminación

### Otra iteración

1. agregar js para poder hacer los select como autocompletar (editable). La solución por ahora es usar un datalist para que se comporte como autocompletar, pero de esta manera no puedo usar el id de las categorías sino leer el valor mostrado.
1. crear colección de grupos. ¿Separar categorías de grupos?
1. crud para categorías y grupos
1. agregar cuentas de usuario
1. una página de perfil sólo para modificar el nombre para mostrar
1. según la cuenta figura el responsable por defecto
1. agregar un registro de ingresos también
1. selectores de fechas para el home (requiere javascript)
1. eliminación masiva con un rango de fechas (o tal vez con cajas de selección pero no lo veo relevante, nos sirve más por fechas)
1. borrado de datos mayores a dos meses
1. Refactoring models con una clase común. ¿Tal vez poner create y update en un método write que valide el id?