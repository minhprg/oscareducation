'use strict';

const wget = ( item ) => {
    try { return JSON.parse(window.localStorage.getItem(item)); }
    catch (error) { return null; }
}

const wset = ( key, value ) => {
    window.localStorage.setItem(key, JSON.stringify(value));
}

class Messenger
{
    constructor()
    {
        this.update = wget('update') ? new Date(wget('update')) : new Date(0);
        this.expressions = [];

        let exprs = wget('expressions') ? wget('expressions') : [];
        for (let e of exprs)
        { this.expressions[e.id] = e; }
    }

    check()
    {
        let self = this;

        return new Promise( ( resolve, reject ) => {
            $.ajax({
                url: "/algebra/api/updated",
                contentType: "application/json"
            }).done( resolve ).fail( reject );
        });
    }

    fetch()
    {
        let self              = this;
        let backendLastUpdate = new Date(0);

        return new Promise( ( resolve, reject ) => {

            this.check()
                .then( ( response ) => {
                    backendLastUpdate = new Date(response.date);
                }).catch( console.log );

            if (backendLastUpdate < self.update)
            { return resolve(self.expressions); }

            $.ajax({
                url: "/algebra/api/expressions",
                data: { since: self.update.getTime() },
                contentType: "application/json"
            }).done( ( response ) => {
                let promises = [];

                for (let id of response.ids)
                {
                    promises.push( new Promise( ( resolve, reject ) => {
                        $.ajax({
                            url: "/algebra/api/expression/" + id,
                            contentType: "application/json"
                        }).done( ( response ) => {
                            self.expressions[
                                response.expression.id
                            ] = response.expression;
                            resolve(response.expression);
                        }).fail(reject);
                    }));
                }

                Promise.all(promises).then( (x) => {
                    self.update = backendLastUpdate;
                    console.log("UPDATE: " + backendLastUpdate);
                    resolve(x);
                }).catch(reject);

            }).fail( reject );
        });
    }

    save()
    {
        let self = this;
        let exprs = self.expressions.filter( (e) => { return e; } );

        wset('expressions', exprs);
        wset('update', this.update.getTime());
    }
}
