from restless.preparers import FieldsPreparer, CollectionSubPreparer

client_preparer = FieldsPreparer(fields={
    'id': 'id',
    'full_name': 'full_name',
})


# Then, in the main preparer, pull them in using `SubPreparer`.
room_preparer = FieldsPreparer(fields={
    'clients': CollectionSubPreparer('clients', client_preparer),
    'number': 'number',
})

hotel_preparer = FieldsPreparer(fields={
    'title': 'title',
    'rooms': CollectionSubPreparer('rooms', room_preparer)
})