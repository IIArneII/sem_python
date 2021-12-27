import {MongoClient, ObjectId} from "mongodb";
import express from "express";
import * as inquiry from "./inquiry.js";

function transform(str){
    let num = /^\d+.?\d*$/
    let date = /^\d{4}-\d\d-\d\d$/
    if(num.test(str))
        return Number(str)
    if(date.test(str))
        return new Date(str)
    return str
}

/*
*r - регулярное выражение
*b - между
*l - меньше или равно
*g - больше или равно 
*/

function make_match(match){
    let matchDB = {}
    for(let i in match){
        if(i.includes('*')){
            let keys = i.split('*')
            if(keys[1] == 'r') matchDB[keys[0]] = {$regex: new RegExp(match[i], "i")};
            if(keys[1] == 'b'){
                let b = match[i].split('*');
                if(!('$and' in matchDB)){
                    matchDB['$and'] = [];
                }
                matchDB['$and'].push({[keys[0]]: {$gte: transform(b[0])}});
                matchDB['$and'].push({[keys[0]]: {$lte: transform(b[1])}});
            }
            if(keys[1] == 'l') matchDB[keys[0]] = {$lte: transform(match[i])};
            if(keys[1] == 'g') matchDB[keys[0]] = {$gte: transform(match[i])};
        }
        else if(i == '_id') matchDB[i] = new ObjectId(match[i])
        else matchDB[i] = transform(match[i])
    }
    return matchDB
}

function make_proj(proj){
    if(!proj){
        if(!Array.isArray(proj)) proj = [proj];
        let projDB = {};
        for(let i of proj){
            projDB[i] = 1;
        }
        if(!proj.includes('_id')) projDB['_id'] = 0;
        return projDB
    }
    else return null
}

function make_set(set, coll){
    if(coll != 'LibraryCards'){
        for(let i in set){
            if(Array.isArray(set[i])){
                for(let j in set[i]){
                    set[i][j] = new ObjectId(set[i][j])
                }
            }
            set[i] = transform(set[i])
            if(coll == 'Publications' && i == 'p_year'){
                set[i] = transform(set[i].toString() + '-' + '01' + '-' + '01')
            }
        }
    }
    else{
        for(let i in set){
            if(Array.isArray(set[i])){
                for(let j in set[i]){
                    set[i][j]['librarian'] = new ObjectId(set[i][j]['librarian'])
                    set[i][j]['item'] = new ObjectId(set[i][j]['item'])
                    let d = transform(set[i][j]['issue_date']).split('.')
                    set[i][j]['issue_date'] = transform(d[2] + '-' + d[1] + '-' + d[0])
                    d = transform(set[i][j]['deadline_date']).split('.')
                    set[i][j]['deadline_date'] = transform(d[2] + '-' + d[1] + '-' + d[0])
                    if(set[i][j]['return_date']){
                        d = transform(set[i][j]['return_date']).split('.')
                        set[i][j]['return_date'] = transform(d[2] + '-' + d[1] + '-' + d[0])
                    }
                    else set[i][j]['return_date'] = null
                }
            }
            set[i] = transform(set[i])
        }
    }
    return set
}

const nameUserDB = "Arne";
const passwordDB = "Qwerty123";
const nameDB = "SemBase";

const app = express();
//const parser = express.urlencoded({extended: false});
const parser = express.json();
const mongoClient = new MongoClient(`mongodb+srv://${nameUserDB}:${passwordDB}@cluster0.apwij.mongodb.net/?retryWrites=true&w=majority`);
var db = null

async function run(){
    try{
        await mongoClient.connect();
        db = mongoClient.db(nameDB);
        console.log('DB Connected')
    }
    catch(err){
        console.log(err);
    }
}
run();


app.get("/", async (request, response)=>{
    console.log("get");
    try{
        if(request.query.type == 'find'){
            let coll = request.query.coll
            let proj = request.query.proj;
            let match = request.query;
            delete match.coll;
            delete match.proj;
            delete match.type;

            match = make_match(match);
            proj = make_proj(proj);
            let data
            if(!proj) data = await db.collection(coll).aggregate([{$match: match}, {$project: proj}]).toArray();
            else data = await db.collection(coll).aggregate([{$match: match}]).toArray();
            response.send(data);
        }
        if(request.query.type == 'collection_list'){
            let data = await db.listCollections().toArray();
            let resp = []
            for(let i of data){
                resp.push(i.name)
            }
            response.send(resp);
        }
        if(request.query.type == 'publication_list'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.publication_list
            inq[4]['$match'] = match

            let data = await db.collection('Publications').aggregate(inq).toArray();
            response.send(data);
        }
        if(request.query.type == 'publication_doc'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.publication_doc;
            inq[0]['$match'] = match;

            let data = await db.collection('Publications').aggregate(inq).toArray();

            response.send(data);
        }
        if(request.query.type == 'racks_list'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.racks_list
            inq[2]['$match'] = match

            let data = await db.collection('Racks').aggregate(inq).toArray();
            response.send(data);
        }
        if(request.query.type == 'racks_doc'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.racks_doc;
            inq[0]['$match'] = match;

            let data = await db.collection('Racks').aggregate(inq).toArray();

            response.send(data);
        }
        if(request.query.type == 'storages_list'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.storages_list
            inq[2]['$match'] = match

            let data = await db.collection('Storages').aggregate(inq).toArray();
            response.send(data);
        }
        if(request.query.type == 'storages_doc'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.storages_doc;
            inq[0]['$match'] = match;

            let data = await db.collection('Storages').aggregate(inq).toArray();

            response.send(data);
        }
        if(request.query.type == 'shelfs_list'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.shelfs_list
            inq[2]['$match'] = match

            let data = await db.collection('Shelfs').aggregate(inq).toArray();
            response.send(data);
        }
        if(request.query.type == 'shelfs_doc'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.shelfs_doc;
            inq[0]['$match'] = match;

            let data = await db.collection('Shelfs').aggregate(inq).toArray();

            response.send(data);
        }
        if(request.query.type == 'fund_items_list'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.fund_items_list
            inq[1]['$match'] = match

            let data = await db.collection('FundItems').aggregate(inq).toArray();
            response.send(data);
        }
        if(request.query.type == 'fund_items_doc'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.fund_items_doc;
            inq[0]['$match'] = match;

            let data = await db.collection('FundItems').aggregate(inq).toArray();

            response.send(data);
        }
        if(request.query.type == 'librarians_list'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.librarians_list
            inq[1]['$match'] = match
            let data = await db.collection('Librarians').aggregate(inq).toArray();
            response.send(data);
        }
        if(request.query.type == 'librarians_doc'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.librarians_doc;
            inq[0]['$match'] = match;

            let data = await db.collection('Librarians').aggregate(inq).toArray();

            response.send(data);
        }
        if(request.query.type == 'authors_list'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.authors_list
            inq[1]['$match'] = match
            let data = await db.collection('Authors').aggregate(inq).toArray();
            response.send(data);
        }
        if(request.query.type == 'authors_doc'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.authors_doc;
            inq[0]['$match'] = match;

            let data = await db.collection('Authors').aggregate(inq).toArray();

            response.send(data);
        }
        if(request.query.type == 'reading_rooms_list'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.reading_rooms_list
            inq[3]['$match'] = match
            let data = await db.collection('ReadingRooms').aggregate(inq).toArray();
            response.send(data);
        }
        if(request.query.type == 'reading_rooms_doc'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.reading_rooms_doc;
            inq[0]['$match'] = match;

            let data = await db.collection('ReadingRooms').aggregate(inq).toArray();

            response.send(data);
        }
        if(request.query.type == 'libraries_list'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.libraries_list
            inq[4]['$match'] = match
            let data = await db.collection('Libraries').aggregate(inq).toArray();
            response.send(data);
        }
        if(request.query.type == 'libraries_doc'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.libraries_doc;
            inq[0]['$match'] = match;

            let data = await db.collection('Libraries').aggregate(inq).toArray();

            response.send(data);
        }
        if(request.query.type == 'library_cards_list'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.library_cards_list
            inq[1]['$match'] = match
            let data = await db.collection('LibraryCards').aggregate(inq).toArray();
            response.send(data);
        }
        if(request.query.type == 'library_cards_doc'){
            let match = request.query;
            delete match.type;
            match = make_match(match);
            let inq = inquiry.library_cards_doc;
            inq[0]['$match'] = match;

            let data = await db.collection('LibraryCards').aggregate(inq).toArray();

            response.send(data);
        }
    }
    catch(err){
        response.status(400).send();
        console.log(err);
    }
});

app.post("/", parser, async (request, response)=>{
    console.log("post");
    console.log(request.body)
    let coll = request.query.coll
    let _id = new ObjectId(request.body._id)
    let set = request.body
    delete set._id
    set = make_set(set, coll)
    let data = await db.collection(coll).updateOne({_id: _id}, {$set: set});;
    response.send(data);
    response.send([])
});

app.put("/", parser, async (request, response)=>{
    console.log("put");
    let coll = request.query.coll
    var inq = inquiry.insert[coll];
    let data = await db.collection(coll).insertOne(inq);
    response.send(data.insertedId);
});

app.delete("/", async (request, response)=>{
    console.log("del");
    let coll = request.query.coll
    let match = request.query;
    delete match.coll;

    match = make_match(match);
    let data = await db.collection(coll).findOneAndDelete(match);
    response.send(data);
});

app.listen(3000);