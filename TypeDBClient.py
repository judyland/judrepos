from typedb.client import TypeDB, SessionType, TransactionType
keyspace = "haganash"

def queryEntities():
    with TypeDB.core_client("localhost:1729") as client:
        with client.session(keyspace,SessionType.DATA) as session:
            with session.transaction(TransactionType.READ) as transaction:
               answer_it  = transaction.query().match("match $ent isa entity, has name $name; get $name;")
               entityNames = []
               for ans in answer_it:
                   entity = ans.get("name")
                   print("entity retrieved " + entity.get_value())

                   entityNames.append(entity.get_value())

               return entityNames

def queryAttr(entity, attr):
    with TypeDB.core_client("localhost:1729") as client:
        with client.session(keyspace,SessionType.DATA) as session:
            with session.transaction(TransactionType.READ) as transaction:
                querystr = 'match $ent isa entity, has name "' + str(entity) + '", has ' + attr + ' $attr; get $attr;'
                print(querystr)
                answer_it = transaction.query().match(querystr)
                attrVal = 0.0
                for ans in answer_it:
                   attrVal = ans.get("attr").get_value()
                   #attrVal = attrVal.get_value()
                return attrVal

def parseTql(file):
    with open(file) as f:
        lines = f.readlines()
    Entities = ['entity']
    Relations = ['relation']
    for i in lines:
        words = i.split(' ')
        print(words)
        for i in range(len(words)):
            w = words[i]
            w = w.split(';')[0]
            w = w.split(',')[0]
            if w in Entities:
                Entities.append(words[i - 2])
            if w in Relations:
                Relations.append(words[i - 2])


    return Entities, Relations
