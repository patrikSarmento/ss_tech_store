from django.shortcuts import render, redirect
from .dados_usuarios import usuarios  # dicionário fixo de usuários

# Produtos fixos simulados
produtos = [
    {"nome": "monitor", "categoria": "monitores", "preco": 900, "imagem": "monitor.jpeg"},
    {"nome": "teclado mecanico rgb", "categoria": "teclados", "preco": 200, "imagem": "teclado-mecanico-rgb.jpeg"},
    {"nome": "mouse gamer", "categoria": "mouses", "preco": 150, "imagem": "mouse-gamer.jpeg"},
    {"nome": "fone headset usb", "categoria": "fones", "preco": 250, "imagem": "fone-headset-usb.jpeg"},
    {"nome": "placa de vídeo gtx 1660", "categoria": "pecas", "preco": 1700, "imagem": "placa-video-gtx1660.jpeg"},
]

def index(request):
    # Renderiza a página inicial com os produtos
    return render(request, 'loja/index.html', {'produtos': produtos})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        # Valida se o usuário existe e se a senha bate
        if email in usuarios and usuarios[email]['senha'] == senha:
            request.session['usuario'] = email
            return redirect('index')  # <-- Aqui redireciona para index após login
        # Caso falhe, retorna com erro
        return render(request, 'loja/login.html', {'erro': 'Credenciais inválidas'})
    # Se GET, apenas renderiza o formulário
    return render(request, 'loja/login.html')

def cadastro_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        # Verifica se email já existe no dicionário
        if email in usuarios:
            return render(request, 'loja/cadastro.html', {'erro': 'Email já cadastrado'})
        # Cadastra o usuário novo
        usuarios[email] = {'nome': nome, 'senha': senha}
        return redirect('login')
    # Se GET, apenas renderiza o formulário
    return render(request, 'loja/cadastro.html')

def dashboard(request):
    # Verifica se usuário está logado
    if 'usuario' not in request.session:
        return redirect('login')
    email = request.session['usuario']
    nome = usuarios.get(email, {}).get('nome', 'Usuário')
    # Renderiza a dashboard com o nome do usuário
    return render(request, 'loja/dashboard.html', {'nome': nome})

def logout_view(request):
    # Limpa a sessão e redireciona para index
    request.session.flush()
    return redirect('index')
