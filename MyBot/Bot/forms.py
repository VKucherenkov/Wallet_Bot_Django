from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from Bot.models import MyUser, OperationUser, CategoryOperation, CardUser, Recipient, TypeOperation, BankCard


class RegisterUserForm(UserCreationForm):
    MALE = 'M'
    FEMALE = 'Ж'
    GENDER_CHOICES = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    ]
    username = forms.IntegerField(label='Логин', widget=forms.NumberInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Пол')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'first_name', 'last_name', 'gender', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.IntegerField(label='Логин', widget=forms.NumberInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ProfileUpdateForm(forms.ModelForm):
    MALE = 'M'
    FEMALE = 'Ж'
    GENDER_CHOICES = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    ]
    username = forms.IntegerField(label='Логин', widget=forms.NumberInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Пол')

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'birth_date']


class AddCardForm(forms.ModelForm):
    DEBET = 'дебетовая'
    CREDIT = 'кредитная'
    TYPE_CHOICES = [
        (DEBET, 'дебетовая'),
        (CREDIT, 'кредитная')
    ]

    class Meta:
        model = CardUser
        fields = ['bank', 'type_card', 'credit_limit', 'name_card', 'number_card', 'balans_card']

    bank = forms.ModelChoiceField(
        label='Выберете банк эмитент карты',
        required=True,
        queryset=BankCard.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Выбрать/добавить банк",
    )
    type_card = forms.ChoiceField(
        required=True,
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def clean_number_card(self):
        number_card = self.cleaned_data.get('number_card')
        if len(str(number_card)) != 4 or not str(number_card).isdigit():
            raise forms.ValidationError("Номер карты должен состоять исключительно из четырех цифр.")
        return number_card


class AddBankForm(forms.ModelForm):
    class Meta:
        model = BankCard
        fields = ['name_bank']


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryOperation
        fields = ['type', 'name_cat']

    type = forms.ModelChoiceField(
        label='Выберете тип операции',
        required=True,
        queryset=TypeOperation.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Выбрать/добавить тип операции",
    )


class AddRecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['name_recipient', ]


class AddTypeForm(forms.ModelForm):
    class Meta:
        model = TypeOperation
        fields = ['name_type', ]


class AddOperationForm(forms.ModelForm):
    class Meta:
        model = OperationUser
        fields = ['card', 'category', 'recipient', 'datetime_amount', 'amount_operation', 'balans', 'note_operation']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлечение пользователя
        super().__init__(*args, **kwargs)
        self.query_card = CardUser.objects.filter(telegram_user__telegram_id=user.username)
        if user:
            self.fields['card'] = forms.ModelChoiceField(
                label='Выберите карту списания',
                required=False,
                queryset=self.query_card,
                widget=forms.Select(attrs={'class': 'form-control'}),
                empty_label="Выбрать/добавить карту",
            )

    category = forms.ModelChoiceField(
        label='Выберете категорию операции',
        required=False,
        queryset=CategoryOperation.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Выбрать/добавить категорию",
    )
    datetime_amount = forms.DateTimeField(
        label='Время операции',
        widget=forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'})
    )
    amount_operation = forms.DecimalField(
        label='Сумма по операции',
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-input'})
    )
    balans = forms.DecimalField(
        label='Баланс после операции',
        widget=forms.NumberInput(attrs={'class': 'form-input'})
    )
    recipient = forms.ModelChoiceField(
        label='Выберете получателя',
        required=False,
        queryset=Recipient.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Выбрать/добавить получателя",
    )
    note_operation = forms.CharField(
        label='Описание операции',
        widget=forms.Textarea(attrs={'class': 'form-input', 'rows': 3})
    )

    def clean_amount_operation(self):
        """Валидация суммы операции."""
        amount = self.cleaned_data.get('amount_operation')
        if float(amount) <= 0:
            raise forms.ValidationError("Сумма операции должна быть положительной.")
        return amount

    def clean_balans(self):
        """Валидация баланса по операции."""
        if self.cleaned_data.get('amount_operation') and self.cleaned_data.get(
                'category').type.name_type == 'Тип операции: расход':
            amount = float(self.cleaned_data.get('amount_operation'))
            balans = float(self.cleaned_data.get('balans'))
            if self.cleaned_data.get('card'):
                number_card = self.cleaned_data.get('card').number_card
                balanse_card = float(CardUser.objects.get(number_card=number_card).balans_card)
            else:
                balanse_card = float(self.data.get('balans_card'))
            if balanse_card - amount != balans:
                raise forms.ValidationError(f'Неверный баланс после операции: баланс по операции = {balans};\n'
                                            f'Правильный баланс: {balanse_card} - {amount} = {balanse_card - amount}\n'
                                            f'Разница: {balanse_card - amount - balans}')
        elif self.cleaned_data.get('amount_operation') and self.cleaned_data.get(
                'category').type.name_type == 'Тип операции: доход':
            amount = float(self.cleaned_data.get('amount_operation'))
            balans = float(self.cleaned_data.get('balans'))
            if self.cleaned_data.get('card'):
                number_card = self.cleaned_data.get('card').number_card
                balanse_card = float(CardUser.objects.get(number_card=number_card).balans_card)
            else:
                balanse_card = float(self.data.get('balans_card'))
            if balanse_card + amount != balans:
                raise forms.ValidationError(f'Неверный баланс после операции: баланс по операции = {balans};\n'
                                            f'Правильный баланс: {balanse_card} + {amount} = {balanse_card + amount}\n'
                                            f'Разница: {balanse_card + amount - balans}')
        return self.cleaned_data.get('balans')
