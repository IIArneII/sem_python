var publication_list = [
    {$unwind: {
        path: "$authors",
        preserveNullAndEmptyArrays: true
    }},
    {$lookup:{
        from: "Authors",
        localField: "authors",
        foreignField: "_id",
        as: "authors"
    }},
    {$group:{
        _id: {_id: "$_id", name: "$name", pages: "$pages", p_year: "$p_year", category: "$category"},
        authors:{
            $addToSet:{
                $concat: [{$arrayElemAt: ["$authors.first_name", 0]}, ' ', {$arrayElemAt: ["$authors.last_name", 0]}]
            }
        }
    }},
    {$project:{
        _id: {$toString: "$_id._id"},
        name: "$_id.name",
        category: "$_id.category",
        authors: "$authors",
        pages: "$_id.pages",
        p_year: {$year: "$_id.p_year"}
    }},
    {$match: {}},
    {$sort: {
        name: 1
    }}
];

var publication_doc = [
    {$match: {}},
    {$unwind: {
        path: "$authors",
        preserveNullAndEmptyArrays: true
    }},
    {$unwind: {
        path: "$items",
        preserveNullAndEmptyArrays: true
    }},
    {$lookup:{
        from: "Authors",
        localField: "authors",
        foreignField: "_id",
        as: "authors"
    }},
    {$lookup:{
        from: "FundItems",
        localField: "items",
        foreignField: "_id",
        as: "items"
    }},
    {$group:{
        _id: {_id: "$_id", name: "$name", pages: "$pages", p_year: "$p_year", category: "$category", receipt_date: "$receipt_date", attributes: "$attributes"},
        authors:{
            $addToSet:{
                _id: {$arrayElemAt: ["$authors._id", 0]},
                first_name: {$arrayElemAt: ["$authors.first_name", 0]},
                last_name: {$arrayElemAt: ["$authors.last_name", 0]}
            }
        },
        items:{
            $addToSet:{
                _id: {$arrayElemAt: ["$items._id", 0]},
                item_number: {$arrayElemAt: ["$items.item_number", 0]},
            }
        }
    }},
    {$project:{
        _id: "$_id._id",
        name: "$_id.name",
        category: "$_id.category",
        pages: "$_id.pages",
        p_year: {$year: "$_id.p_year"},
        receipt_date: "$_id.receipt_date",
        authors: "$authors",
        items: "$items",
        attributes: {$objectToArray: "$_id.attributes"}
    }}
];

var racks_list = [
    {$unwind: {
        path: "$shelfs",
        preserveNullAndEmptyArrays: true
    }},
    {$group:{
        _id: {$toString: "$_id"},
        shelfs:{
            $addToSet: {$toString: "$shelfs"}
        }
    }},
    {$match: {}}
];

var racks_doc = [
    {$match: {}},
    {$unwind: {
        path: "$shelfs",
        preserveNullAndEmptyArrays: true
    }},
    {$group:{
        _id: "$_id",
        shelfs:{
            $addToSet: {_id: "$shelfs"}
        }
    }}
];

var storages_list = [
    {$unwind: {
        path: "$racks",
        preserveNullAndEmptyArrays: true
    }},
    {$group:{
        _id: {$toString: "$_id"},
        racks:{
            $addToSet: {$toString: "$racks"}
        }
    }},
    {$match: {}}
];

var storages_doc = [
    {$match: {}},
    {$unwind: {
        path: "$racks",
        preserveNullAndEmptyArrays: true
    }},
    {$group:{
        _id: "$_id",
        racks:{
            $addToSet: {_id: "$racks"}
        }
    }}
];

var shelfs_list = [
    {$unwind: {
        path: "$items",
        preserveNullAndEmptyArrays: true
    }},
    {$group:{
        _id: {$toString: "$_id"},
        items:{
            $addToSet: {$toString: "$items"}
        }
    }},
    {$match: {}}
];

var shelfs_doc = [
    {$match: {}},
    {$unwind: {
        path: "$items",
        preserveNullAndEmptyArrays: true
    }},
    {$lookup:{
        from: "FundItems",
        localField: "items",
        foreignField: "_id",
        as: "items"
    }},
    {$lookup:{
        from: "Publications",
        localField: "items._id",
        foreignField: "items",
        as: "publication"
    }},
    {$group:{
        _id: "$_id",
        items:{
            $addToSet: {
                _id: {$arrayElemAt: ["$items._id", 0]},
                item_number: {$arrayElemAt: ["$items.item_number", 0]},
                publication: {$arrayElemAt: ["$publication.name", 0]}
            }
        }
    }}
];

var fund_items_list = [
    {$set: {_id: {$toString: "$_id"}}},
    {$match: {}}
];

var fund_items_doc = [
    {$match: {}}
];

var librarians_list = [
    {$set: {_id: {$toString: "$_id"}}},
    {$match: {}}
];

var librarians_doc = [
    {$match: {}}
];

var authors_list = [
    {$set: {_id: {$toString: "$_id"}}},
    {$match: {}}
];

var authors_doc = [
    {$match: {}}
];

var reading_rooms_list = [
    {$unwind: {
        path: "$librarians",
        preserveNullAndEmptyArrays: true
    }},
    {$lookup:{
        from: "Librarians",
        localField: "librarians",
        foreignField: "_id",
        as: "librarians"
    }},
    {$group:{
        _id: {$toString: "$_id"},
        librarians:{
            $addToSet:{
                $concat: [{$arrayElemAt: ["$librarians.first_name", 0]}, ' ', {$arrayElemAt: ["$librarians.last_name", 0]}]
            }
        }
    }},
    {$match: {}}
];

var reading_rooms_doc = [
    {$match: {}},
    {$unwind: {
        path: "$librarians",
        preserveNullAndEmptyArrays: true
    }},
    {$unwind: {
        path: "$items",
        preserveNullAndEmptyArrays: true
    }},
    {$lookup:{
        from: "Librarians",
        localField: "librarians",
        foreignField: "_id",
        as: "librarians"
    }},
    {$lookup:{
        from: "FundItems",
        localField: "items",
        foreignField: "_id",
        as: "items"
    }},
    {$group:{
        _id: "$_id",
        librarians:{
            $addToSet:{
                _id: {$arrayElemAt: ["$librarians._id", 0]},
                first_name: {$arrayElemAt: ["$librarians.first_name", 0]},
                last_name: {$arrayElemAt: ["$librarians.last_name", 0]}
            }
        },
        items:{
            $addToSet:{
                _id: {$arrayElemAt: ["$items._id", 0]},
                item_number: {$arrayElemAt: ["$items.item_number", 0]},
            }
        }
    }}
];

var libraries_list = [
    {$unwind: {
        path: "$cards",
        preserveNullAndEmptyArrays: true
    }},
    {$lookup:{
        from: "LibraryCards",
        localField: "cards",
        foreignField: "_id",
        as: "cards"
    }},
    {$group:{
        _id: {_id: {$toString: "$_id"}, address: "$address"},
        cards:{
            $addToSet:{
                $concat: [{$arrayElemAt: ["$cards.first_name", 0]}, ' ', {$arrayElemAt: ["$cards.last_name", 0]}]
            }
        }
    }},
    {$project:{
        _id: "$_id._id",
        address: "$_id.address",
        cards: "$cards"
    }},
    {$match: {}}
];

var libraries_doc = [
    {$match: {}},
    {$unwind: {
        path: "$cards",
        preserveNullAndEmptyArrays: true
    }},
    {$unwind: {
        path: "$reading_rooms",
        preserveNullAndEmptyArrays: true
    }},
    {$unwind: {
        path: "$storages",
        preserveNullAndEmptyArrays: true
    }},
    {$lookup:{
        from: "LibraryCards",
        localField: "cards",
        foreignField: "_id",
        as: "cards"
    }},
    {$group:{
        _id: {_id: "$_id", address: "$address"},
        cards:{
            $addToSet:{
                _id: {$arrayElemAt: ["$cards._id", 0]},
                first_name: {$arrayElemAt: ["$cards.first_name", 0]},
                last_name: {$arrayElemAt: ["$cards.last_name", 0]}
            }
        },
        reading_rooms:{
            $addToSet:{
                _id: "$reading_rooms"
            }
        },
        storages: {
            $addToSet:{
                _id: "$storages"
            }
        }
    }},
    {$project:{
        _id: "$_id._id",
        address: "$_id.address",
        storages: "$storages",
        reading_rooms: "$reading_rooms",
        cards: "$cards"
    }}
];

var library_cards_list = [
    {$project:{
        _id: {$toString: "$_id"},
        first_name: "$first_name",
        last_name: "$last_name",
        category: "$category",
        registration_date: "$registration_date"
    }},
    {$match: {}}
];

var library_cards_doc = [
    {$match: {}},
    {$unwind: {
        path: "$rows",
        preserveNullAndEmptyArrays: true
    }},
    {$lookup:{
        from: "Publications",
        localField: "rows.item",
        foreignField: "items",
        as: "rows.publication"
    }},
    {$group:{
        _id: {_id: "$_id", first_name: "$first_name", last_name: "$last_name", birth_date: "$birth_date",
              address: "$address", phone: "$phone", registration_date: "$registration_date", category: "$category", attributes: "$attributes"},
        rows: {
            $addToSet: {
                librarian: "$rows.librarian",
                item: "$rows.item",
                publication: {$arrayElemAt: ["$rows.publication.name", 0]},
                issue_date: "$rows.issue_date",
                deadline_date: "$rows.deadline_date",
                return_date: "$rows.return_date"
            }
        }
    }},
    {$project:{
        _id: "$_id._id",
        first_name: "$_id.first_name",
        last_name: "$_id.last_name",
        registration_date: "$_id.registration_date",
        birth_date: "$_id.birth_date",
        phone: "$_id.phone",
        address: "$_id.address",
        category: "$_id.category",
        attributes: {$objectToArray: "$_id.attributes"},
        rows: "$rows"
    }}
];

//-----------------------------------------------------------------------------------------------------

var insert_authors = {
    first_name: null,
    last_name: null,
    patronymic: null,
    birth_date: new Date(),
    death_date: null
}

var insert_fund_items = {
    item_number: null
}

var insert_librarians = {
    first_name: null,
    last_name: null,
    patronymic: null,
    device_date: new Date(),
    dismissal_date: null
}

var insert_libraries = {
    address: null,
    storages: [],
    reading_rooms:[],
    cards: []
}

var insert_library_cards = {
    first_name: null,
    last_name: null,
    birth_date: new Date(),
    address: null,
    phone: null,
    registration_date: new Date(),
    category: null,
    attributes: {},
    rows: []
}

var insert_publications = {
    name: null,
    pages: null,
    p_year: new Date(),
    authors: [],
    items: [],
    category: null,
    attributes: {},
    receipt_date: new Date()
}

var insert_racks = {
    shelfs: []
}

var insert_reading_rooms = {
    places: null,
    librarians: [],
    items: []
}

var insert_shelfs = {
    items: []
}

var insert_storages = {
    racks: []
}

var insert = {
    Authors: insert_authors,
    Publications: insert_publications,
    LibraryCards: insert_library_cards,
    Libraries: insert_libraries,
    Librarians: insert_librarians,
    FundItems: insert_fund_items,
    Storages: insert_storages,
    Shelfs: insert_shelfs,
    ReadingRooms: insert_reading_rooms,
    Racks: insert_racks
}

export {publication_list, publication_doc, racks_list, racks_doc, storages_doc, storages_list, shelfs_doc, shelfs_list, fund_items_doc, fund_items_list,
librarians_doc, librarians_list, authors_doc, authors_list, reading_rooms_doc, reading_rooms_list, libraries_doc, libraries_list, library_cards_list, library_cards_doc,
insert};