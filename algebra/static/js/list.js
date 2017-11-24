'use strict';

const MQ = MathQuill.getInterface(2);
const messenger = new Messenger();
let forms = [];

function makeForm( link )
{
    $("#expression-list a").removeClass('active');
    $( link ).addClass('active');

    let id = $( link ).attr('id').split('-')[2];
    let expression = messenger.expressions[id];
    let $form = $(`
      <form id='js-expr-form-${id}' class='expression-form' onsubmit='submitForm(this)'>
          <div class='form-group'>
              <label for'expression'>Expression</label>
              <input type='text' name='expression' class='form-control'
               value='${expression.expression}' required>
          </div>
          <div class='form-group'>
              <label for'solution'>Solution</label>
              <input type='text' name='solution' class='form-control'
               value='${expression.solution}' required>
          </div>
          <div class='form-group'>
              <label for'solution'>Type</label>
              <input type='text' name='type' class='form-control'
               value='${expression.expression_type}' required>
          </div>
          <div class='form-group'>
              <label for'level'>Level</label>
              <input type='text' name='level' class='form-control'
               value='${expression.level}' required>
          </div>

          <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    `);

    $("#expression-form form").remove();
    $("#expression-form #expression-form-placeholder").remove();
    $("#expression-form").append($form);
}

function submitForm( form )
{
    let $form = $( form );
    let formId = $form.attr('id').split('-');
    let url = "/algebra/api/expression"

    if (formId.length == 4) // modification
    { url += "/" + formId[3]; }

    let expression = $('input[name="expression"]', $form).val();
    let solution = $('input[name="solution"]', $form).val();
    let level = $('input[name="level"]', $form).val();
    let type = $('input[name="type"]', $form).val();

    $.ajax({
        url: url,
        contentType: "application/json",
        data: {
            expression: expression,
            solution: solution,
            level: level,
            type: type
        }
    }).done(console.log).fail(console.log);
}

$(document).ready( () => {
    messenger.fetch().then( function(data)
    {
        let $dom = $( '#expression-list' );
        messenger.expressions.forEach( function( e )
        {
            $dom.append(
                $("<a href='#' class='list-group-item' id='js-expr-"
                + e.id + "' onclick='makeForm(this)'>" + e.expression + "</a>")
            );
        });
    }).catch( console.log );
});
