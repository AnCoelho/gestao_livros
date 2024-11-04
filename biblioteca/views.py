
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from datetime import date, timedelta
from django.db.models import Count  # Import necessário para contagem de livros por autor
from .models import Autor, Livro
from .serializers import AutorSerializer, LivroSerializer

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

    def create(self, request, *args, **kwargs):
        if Autor.objects.filter(nome=request.data.get('nome')).exists():
            return Response({"detail": "Autor já existe."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'autor__nome']

    # Método customizado para atualizar o título de um livro
    @action(detail=True, methods=['patch'])
    def atualizar_titulo(self, request, pk=None):
        livro = self.get_object()
        livro.titulo = request.data.get('titulo')
        livro.save()
        return Response({'status': 'Título atualizado!'})

    # Método customizado para listar livros publicados no último ano
    @action(detail=False, methods=['get'])
    def publicados_ultimo_ano(self, request):
        um_ano_atras = date.today() - timedelta(days=365)  # Calcula a data de um ano atrás
        livros = Livro.objects.filter(data_publicacao__gte=um_ano_atras)  # Filtra livros
        serializer = self.get_serializer(livros, many=True)
        return Response(serializer.data)

    # Novo método customizado para retornar a quantidade total de livros e livros por autor
    @action(detail=False, methods=['get'])
    def quantidade_livros(self, request):
        # Obtém a quantidade total de livros
        total_livros = Livro.objects.count()

        # Obtém a quantidade de livros por autor
        livros_por_autor = Autor.objects.annotate(total_livros=Count('livros')).values('nome', 'total_livros')

        # Cria a resposta com as informações coletadas
        return Response({
            'total_livros': total_livros,
            'livros_por_autor': list(livros_por_autor)
        })
