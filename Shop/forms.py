from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["ReceiverName", "Phone", "Address", "PaymentMethod", "Remark"]
        labels = {
            "ReceiverName": "收货人",
            "Phone": "联系电话",
            "Address": "收货地址",
            "PaymentMethod": "支付方式",
            "Remark": "订单备注",
        }
        widgets = {
            "ReceiverName": forms.TextInput(attrs={"placeholder": "请输入姓名"}),
            "Phone": forms.TextInput(attrs={"placeholder": "请输入手机号"}),
            "Address": forms.TextInput(attrs={"placeholder": "宿舍楼、校区或约定交易地点"}),
            "PaymentMethod": forms.RadioSelect(),
            "Remark": forms.Textarea(attrs={"rows": 3, "placeholder": "可填写交易时间、备注等"}),
        }
