from rest_
    API Guide
    Topics
    Community

    Serializers
    Declaring Serializers
    Serializing objects
    Deserializing objects
    Saving instances
    Validation
    Accessing the initial data and instance
    Partial updates
    Dealing with nested objects
    Writable nested representations
    Dealing with multiple objects
    Including extra context
    ModelSerializer
    Inspecting a ModelSerializer
    Specifying which fields to include
    Specifying nested serialization
    Specifying fields explicitly
    Specifying read only fields
    Additional keyword arguments
    Relational fields
    Customizing field mappings
    HyperlinkedModelSerializer
    Absolute and relative URLs
    How hyperlinked views are determined
    Changing the URL field name
    ListSerializer
    allow_empty
    Customizing ListSerializer behavior
    BaseSerializer
    Read-only BaseSerializer classes
    Read-write BaseSerializer classes
    Creating new base classes
    Advanced serializer usage
    Overriding serialization and deserialization behavior
    Serializer Inheritance
    Dynamically modifying fields
    Customizing the default fields
    Third party packages
    Django REST marshmallow
    Serpy
    MongoengineModelSerializer
    GeoFeatureModelSerializer
    HStoreSerializer
    Dynamic REST
    Dynamic Fields Mixin
    DRF FlexFields
    Serializer Extensions
    HTML JSON Forms
    DRF-Base64
    QueryFields
    DRF Writable Nested

    Real-time error monitoring, alerting, and analytics for developers.

    Fund Django REST framework

serializers.py
Serializers

    Expanding the usefulness of the serializers is something that we would like to address. However, it's not a trivial problem, and it will take some serious design work.

    — Russell Keith-Magee, Django users group

Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types. Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data.

The serializers in REST framework work very similarly to Django's Form and ModelForm classes. We provide a Serializer class which gives you a powerful, generic way to control the output of your responses, as well as a ModelSerializer class which provides a useful shortcut for creating serializers that deal with model instances and querysets.
Declaring Serializers

Let's start by creating a simple object we can use for example purposes:

from datetime import datetime

class Comment(object):
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

comment = Comment(email='leila@example.com', content='foo bar')

We'll declare a serializer that we can use to serialize and deserialize data that corresponds to Comment objects.

Declaring a serializer looks very similar to declaring a form:

from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

Serializing objects

We can now use CommentSerializer to serialize a comment, or list of comments. Again, using the Serializer class looks a lot like using a Form class.

serializer = CommentSerializer(comment)
serializer.data
# {'email': 'leila@example.com', 'content': 'foo bar', 'created': '2016-01-27T15:17:10.375877'}

At this point we've translated the model instance into Python native datatypes. To finalise the serialization process we render the data into json.

from rest_framework.renderers import JSONRenderer

json = JSONRenderer().render(serializer.data)
json
# b'{"email":"leila@example.com","content":"foo bar","created":"2016-01-27T15:17:10.375877"}'

Deserializing objects

Deserialization is similar. First we parse a stream into Python native datatypes...

import io
from rest_framework.parsers import JSONParser

stream = io.BytesIO(json)
data = JSONParser().parse(stream)

...then we restore those native datatypes into a dictionary of validated data.

serializer = CommentSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# {'content': 'foo bar', 'email': 'leila@example.com', 'created': datetime.datetime(2012, 08, 22, 16, 20, 09, 822243)}

Saving instances

If we want to be able to return complete object instances based on the validated data we need to implement one or both of the .create() and .update() methods. For example:

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance

If your object instances correspond to Django models you'll also want to ensure that these methods save the object to the database. For example, if Comment was a Django model, the methods might look like this:

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance

Now when deserializing data, we can call .save() to return an object instance, based on the validated data.

comment = serializer.save()

Calling .save() will either create a new instance, or update an existing instance, depending on if an existing instance was passed when instantiating the serializer class:

# .save() will create a new instance.
serializer = CommentSerializer(data=data)

# .save() will update the existing `comment` instance.
serializer = CommentSerializer(comment, data=data)

Both the .create() and .update() methods are optional. You can implement either neither, one, or both of them, depending on the use-case for your serializer class.
Passing additional attributes to .save()

Sometimes you'll want your view code to be able to inject additional data at the point of saving the instance. This additional data might include information like the current user, the current time, or anything else that is not part of the request data.

You can do so by including additional keyword arguments when calling .save(). For example:

serializer.save(owner=request.user)

Any additional keyword arguments will be included in the validated_data argument when .create() or .update() are called.
Overriding .save() directly.

In some cases the .create() and .update() method names may not be meaningful. For example, in a contact form we may not be creating new instances, but instead sending an email or other message.

In these cases you might instead choose to override .save() directly, as being more readable and meaningful.

For example:

class ContactForm(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField()

    def save(self):
        email = self.validated_data['email']
        message = self.validated_data['message']
        send_email(from=email, message=message)

Note that in the case above we're now having to access the serializer .validated_data property directly.
Validation

When deserializing data, you always need to call is_valid() before attempting to access the validated data, or save an object instance. If any validation errors occur, the .errors property will contain a dictionary representing the resulting error messages. For example:

serializer = CommentSerializer(data={'email': 'foobar', 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'email': ['Enter a valid e-mail address.'], 'created': ['This field is required.']}

Each key in the dictionary will be the field name, and the values will be lists of strings of any error messages corresponding to that field. The non_field_errors key may also be present, and will list any general validation errors. The name of the non_field_errors key may be customized using the NON_FIELD_ERRORS_KEY REST framework setting.

When deserializing a list of items, errors will be returned as a list of dictionaries representing each of the deserialized items.
Raising an exception on invalid data

The .is_valid() method takes an optional raise_exception flag that will cause it to raise a serializers.ValidationError exception if there are validation errors.

These exceptions are automatically dealt with by the default exception handler that REST framework provides, and will return HTTP 400 Bad Request responses by default.

# Return a 400 response if the data was invalid.
serializer.is_valid(raise_exception=True)

Field-level validation

You can specify custom field-level validation by adding .validate_<field_name> methods to your Serializer subclass. These are similar to the .clean_<field_name> methods on Django forms.

These methods take a single argument, which is the field value that requires validation.

Your validate_<field_name> methods should return the validated value or raise a serializers.ValidationError. For example:

from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()

    def validate_title(self, value):
        """
        Check that the blog post is about Django.
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value

Note: If your <field_name> is declared on your serializer with the parameter required=False then this validation step will not take place if the field is not included.
Object-level validation

To do any other validation that requires access to multiple fields, add a method called .validate() to your Serializer subclass. This method takes a single argument, which is a dictionary of field values. It should raise a serializers.ValidationError if necessary, or just return the validated values. For example:

from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    start = serializers.DateTimeField()
    finish = serializers.DateTimeField()

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data

Validators

Individual fields on a serializer can include validators, by declaring them on the field instance, for example:

def multiple_of_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError('Not a multiple of ten')

class GameRecord(serializers.Serializer):
    score = IntegerField(validators=[multiple_of_ten])
    ...

Serializer classes can also include reusable validators that are applied to the complete set of field data. These validators are included by declaring them on an inner Meta class, like so:

class EventSerializer(serializers.Serializer):
    name = serializers.CharField()
    room_number = serializers.IntegerField(choices=[101, 102, 103, 201])
    date = serializers.DateField()

    class Meta:
        # Each room only has one event per day.
        validators = UniqueTogetherValidator(
            queryset=Event.objects.all(),
            fields=['room_number', 'date']
        )

For more information see the validators documentation.
Accessing the initial data and instance

When passing an initial object or queryset to a serializer instance, the object will be made available as .instance. If no initial object is passed then the .instance attribute will be None.

When passing data to a serializer instance, the unmodified data will be made available as .initial_data. If the data keyword argument is not passed then the .initial_data attribute will not exist.
Partial updates

By default, serializers must be passed values for all required fields or they will raise validation errors. You can use the partial argument in order to allow partial updates.

# Update `comment` with partial data
serializer = CommentSerializer(comment, data={'content': 'foo bar'}, partial=True)

Dealing with nested objects

The previous examples are fine for dealing with objects that only have simple datatypes, but sometimes we also need to be able to represent more complex objects, where some of the attributes of an object might not be simple datatypes such as strings, dates or integers.

The Serializer class is itself a type of Field, and can be used to represent relationships where one object type is nested inside another.

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

class CommentSerializer(serializers.Serializer):
    user = UserSerializer()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

If a nested representation may optionally accept the None value you should pass the required=False flag to the nested serializer.

class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)  # May be an anonymous user.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

Similarly if a nested representation should be a list of items, you should pass the many=True flag to the nested serialized.

class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)
    edits = EditItemSerializer(many=True)  # A nested list of 'edit' items.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

Writable nested representations

When dealing with nested representations that support deserializing the data, any errors with nested objects will be nested under the field name of the nested object.

serializer = CommentSerializer(data={'user': {'email': 'foobar', 'username': 'doe'}, 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'user': {'email': ['Enter a valid e-mail address.']}, 'created': ['This field is required.']}

Similarly, the .validated_data property will include nested data structures.
Writing .create() methods for nested representations

If you're supporting writable nested representations you'll need to write .create() or .update() methods that handle saving multiple objects.

The following example demonstrates how you might handle creating a user with a nested profile object.

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']framework import routers
from .api import LeadViewSet

router = routers.DefaultRouter()
router.register('api/leads', LeadViewSet, 'leads')

urlpatterns = router.urls