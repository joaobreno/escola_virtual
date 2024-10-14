from rest_framework import serializers
from .models import *

class EstudanteSerializer(serializers.ModelSerializer):
    matricula = serializers.CharField(required=False, allow_blank=True)
    cursos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Curso.objects.none(),
        required=False
    )

    class Meta:
        model = Estudante
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EstudanteSerializer, self).__init__(*args, **kwargs)
        # Aqui você filtra os cursos com base no request.user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            self.fields['cursos'].queryset = Curso.objects.filter(usuario=request.user)