'use strict';

const MQ = MathQuill.getInterface(2);

function formatExpressions()
{
    let expressions = document.getElementsByClassName( "algebra-expression" );
    for (let expression of expressions)
    { MQ.StaticMath(expression); }
}

function insertExpression( json )
{
    let $expressionList = $(".expression-list tbody");
    let expression = json.expression;

    let $expression = $(
        "<tr>" +
        "<td><div class='algebra-expression'>" + expression.expression + "</div></td>" +
        "<td><input placeholder='1' type='text'></td>" +
        "<td>" + expression.solution + "</td>" +
        "<td>" + expression.expression_type + "</td>" +
        "<td><input checked='checked' value='on' type='checkbox'></td>" +
        "<td><a href='' class='btn btn-primary'>Edit</a></td>" +
        "<td><a href='' class='btn btn-primary btn-danger'>Delete</a></td>" +
        "</tr>"
    );

    $expressionList.append($expression);
}

function getExpression( id )
{
    return new Promise( function( resolve, reject )
    {
        $.get("/algebra/api/expression/" + id)
            .done( resolve )
            .fail( reject );
    });
}

function getExpressions()
{
    return new Promise( function( resolve, reject )
    {    
        $.get("/algebra/api/expressions")
         .done( resolve )
         .fail( reject );
    });
}

function init()
{
    getExpressions()
        .then( ( response ) => {
            let promises = [];
            
            for (let id of response.nb)
            { 
                getExpression(id)
                    .then( insertExpression )
                    .catch( console.log );
            }
        })
        .catch( console.log );
}

$(document).ready( () => {
    init();
});
