from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from src.apps.payment.api.v1.serializer import PaymentSerializer
from src.apps.payment.models import Payment
from src.apps.accounts.models import Purchased_course


class PaymentCreateView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        course_id = serializer.data['course']
        Purchased_course.objects.create(user=self.request.user, course_id=course_id)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
