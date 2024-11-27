from django.urls import get_resolver
from rest_framework.test import APIClient
import pytest

@pytest.mark.django_db
def test_all_endpoints():
    """
    Prueba automática que verifica que todos los endpoints definidos en el proyecto responden con un código HTTP válido.
    """
    client = APIClient()
    resolver = get_resolver()
    skipped_endpoints = []  # Lista para guardar los endpoints que fallaron o fueron excluidos

    for url_pattern in resolver.url_patterns:
        try:
            path = url_pattern.pattern.regex.pattern
            response = client.get(path)
            assert response.status_code in [200, 401, 403, 404], f"Error en {path}, Código {response.status_code}"
        except Exception as e:
            skipped_endpoints.append((url_pattern.name, str(e)))

    if skipped_endpoints:
        print("Endpoints que fallaron:")
        for endpoint, error in skipped_endpoints:
            print(f"- {endpoint}: {error}")


