from django.shortcuts import render, get_object_or_404
from produtos.models import Produto, TIPO_PRODUTO, TIPO_SERVICO
from produtos.forms import ProdutoModelForm, ServicoModelForm
from django.http import HttpResponseRedirect


def listagem_produtos(request):
    produtos = Produto.objects.filter(tipo=TIPO_PRODUTO, excluido =False)
    produtos_dos_vendedores = Produto.objects.all()
    produtos_dos_vendedores = [{
        "vendedor" : {"nome" : "maik"},
        "produtos" : produtos
    }]
    context = {"produtos_dos_vendedores": produtos_dos_vendedores}
    return render(request, "templates/listagem_produtos.html", context)

def detalhamento_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    context = {
        "produto": produto
    }
    return render(request, "templates/detalhamento_produto.html", context)

def cadastrar_produto(request):
    form = ProdutoModelForm()
    context = {
        "form" : form
    }
    if request.method == "GET":
        print("É um GET")
    if request.method == "POST":
        print("É um POST")
        form = ProdutoModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/produtos/")
    return render(request, "templates/cadastrar_produtos.html", context)

def alterar_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    if request.method == "POST":
        form = ProdutoModelForm(request.POST)
        if form.is_valid():
            produto.nome = form.cleaned_data["nome"]
            produto.estoque = form.cleaned_data["estoque"]
            produto.preco = form.cleaned_data["preco"]
            produto.save()
            return HttpResponseRedirect(f"/produtos/{produto.id}")
    form = ProdutoModelForm(instance=produto)
    context = {
        "form": form
    }
    return render(request, "templates/alterar_produto.html", context)

def excluir_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    if request.method == "POST":
        produto.excluido = True
        produto.save()
        return HttpResponseRedirect("/produtos/")
    context = {
        "produto": produto
    }
    return render(request, "templates/excluir_produto.html", context)

def listagem_servicos(request):
    servicos = Produto.objects.filter(tipo=TIPO_SERVICO, excluido =False)

    servicos_dos_vendedores = [{
        "vendedor" : {"nome" : "maik"},
        "servicos" : servicos
    }]
    context = {"servicos_dos_vendedores": servicos_dos_vendedores }
    return render(request, "templates/listagem_servicos.html", context)

def cadastro_servico(request):
    if request.method == "POST":
        form = ServicoModelForm(request.POST)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.tipo = TIPO_SERVICO
            produto.save()
            return HttpResponseRedirect("/servicos/")

    form = ServicoModelForm()
    context = {
        "form" : form
    }
    
    return render(request, "templates/cadastrar_servico.html", context)