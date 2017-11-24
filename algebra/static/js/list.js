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
            <label>Expression</label>
            <span>
              <textarea class="keyboard"></textarea>
              <span class='mathquill' data-keyboard-type= "math-advanced">${expression.expression}</span>
               <input name='expression' class="form-control hidden-math-form" required></input>
            </span>
          </div>
          <div class='form-group'>
              <label for'solution'>Solution</label>
              <span>
                <textarea class="keyboard"></textarea>
                <span class='mathquill' data-keyboard-type= "math-advanced">${expression.solution}</span>
                 <input name='solution' class="form-control hidden-math-form" required></input>
              </span>
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

    // mathquill keyboard
    renderMathquil($(".mathquill"), function(MQ, index, mq) {
      var input = $($(mq).parent().find("input")[0]);
      var mathquill = MQ.MathField(mq, {
        handlers: {
          edit: function() {
            input.val(mathquill.text());
          }
        }
      });

      var keyboard = $($(mq).parent().children()[0]);

      return [mathquill, keyboard]
    });
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
