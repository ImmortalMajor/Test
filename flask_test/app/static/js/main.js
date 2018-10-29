$(document).ready(function() {
    $('#categories').on('click', '> li span',function(){
        $('#category').val($(this).text());
        $('#del_category').toggleClass('hidden');
    });

    $('#category').on('input', function() { $('#del_category').addClass('hidden'); });

    $('#add_category').on('click', function(){
        $.post( "http://" + $(location).attr('host') + "/test/add_cat", {'name': $('#category').val()}, function( data ) {
            $('#category').val('');
            draw_categories(data);
        });
    });

    $('#del_category').on('click', function(){
        $.post( "http://" + $(location).attr('host') + "/test/del_cat", {'name': $('#category').val()}, function( data ) {
           draw_categories(data);
        });
        $('#category').val('');
        $(this).toggleClass('hidden');
    });

    $('#categories').on('click', '> li > div > button', function(){
        category = $(this).attr('cat');
        if (get_catfiles(category).length === 0) {
            $.post( "http://" + $(location).attr('host') + "/test/get_files", {'category': category}, function( data ) {
               draw_category_files(data, category);
            });
        } else {
            get_catfiles_list(category).empty();
        }
    });

    $('#categories').on('click', 'ul > li > div > button', function(){
        file = $(this).attr('file');
        category = $(this).attr('cat');
        $.post( "http://" + $(location).attr('host') + "/test/del_file", {'category': category, 'file': file}, function( data ) {
           draw_category_files(data, category);
        });
    });

    $('#tree').on('click', 'li', function(){
        $.post( "http://" + $(location).attr('host') + "/test/go_to", {'folder': $(this).text()}, function( data ) {
           draw_tree(data);
        });
    });

    $('#drive').on('change', function() {
        $.post( "http://" + $(location).attr('host') + "/test/go_to", {'folder': $(this).val()}, function( data ) {
           draw_tree(data);
        });
    });

    check_categories();
    check_images();
});

function make_draggable(el) {
    $(el).draggable({
        revert:true,
        drag:function () {
            //$(this).addClass("active");
            //$(this).closest("#product").addClass("active");
        },
        stop:function () {
            //$(this).removeClass("active").closest("#product").removeClass("active");
        }
    });
}

function make_droppable(el, on_drop) {
    $(el).droppable({
        tolerance:"touch",
        drop: function (event, ui) {
            var category = $(this).find('span').text(), image = ui.draggable;
            file = $('#path').text() + "\\" + image.first().text();
            $.post( "http://" + $(location).attr('host') + "/test/add_file", {'file': file, 'category': category}, function( data ) {
                if(data == false) { alert("This file is already in category."); }
                else {
                    if (get_catfiles_list(category).text() != '') {draw_category_files(data, category);}
                }
            });
        }
    });
}

function draw_categories(data) {
    if(data.length === 0) {
        $('#categories').empty();
    } else {
        var ul = $('#categories');
        ul.html('');
        for (var i = 0; i < data.length; i++) {
            li = $('<li class="input-group mb-3">' +
                        '<div class="input-group-prepend">' +
                            '<button class="btn btn-dark btn-outline-secondary" cat="' + data[i] + '"> &#8659; </button>' +
                        '</div>' +
                        '<span class="form-control">' + data[i] + '</span>' +
                    '</li>');
            make_droppable(li);
            ul.append(li);
            ul.append('<ul cat="' + data[i] + '"></ul>');
        }
    }
}

function draw_category_files(data, category) {
    var ul;
    $("#categories ul").each(function() {
        if($(this).attr('cat') === category) {
            ul = $(this);
            return;
        }
    });
    ul.html('');
    for(var i = 0; i < data.length; i++) {
        ul.append('<li class="input-group mb-3">' +
            '<div class="input-group-prepend">' +
                '<button class="btn btn-dark btn-outline-secondary" cat="' + category +
                                                            '" file="' + data[i] + '"> - </button>' +
            '</div>' +
            '<textarea class="form-control">' + data[i] + '</textarea>' +
        '</li>');
    }
}

function draw_tree(data) {
    $('#path').html(data.path);
    var tree = $("#tree"), imgs = $("#images");
    tree.html('');
    imgs.html('');

    var folders = data.folders;
    var images = data.images;
    if(data.path.length > 3) {
        folders.unshift('..');
    }

    for (var i = 0; i < folders.length; i++) {
        tree.append("<li class='list-group-item'><span class='navbar-link'>" + folders[i] + "</span></li>");
    }
    for (var i = 0; i < images.length; i++) {
        li = $('<li class="btn btn-light">' + images[i] + '</li>');
        make_draggable(li);
        imgs.append(li);
    }
}

function check_images() {
    $("#images li").each(function() {
        make_draggable(this);
    });
}

function check_categories() {
    $("#categories li").each(function() {
        make_droppable(this);
    });
}

function get_catfiles(cat) {
    return get_catfiles_list(cat).find('> li');
}

function get_catfiles_list(cat) {
    var category;
    $("#categories > ul").each(function() {
        if($(this).attr('cat') === cat) { category = $(this); }
    });
    return category;
}
