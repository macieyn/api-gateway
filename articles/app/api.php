<?php

$articles = array(
    'data' => array(
        0 => array(
            'title' => 'The Future of Microservices',
            'description' => 'Annonymous article about what future brings for Web Developers and Internet Users'
        ),
        1 => array(
            'title' => 'PHP is dead',
            'description' => 'PHP is just like punk rock. It can\'t die, but it will be growing'
        )
    )
);

$request = $_REQUEST;

echo json_encode($articles);
