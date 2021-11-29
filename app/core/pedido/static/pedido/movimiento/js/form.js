

function validar_formulario() {

    // document.addEventListener('DOMContentLoaded', function (e) {
        const form = document.getElementById('modal-movimiento');
        const fv = FormValidation.formValidation(form, {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                nro_pedido: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 8,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    obj: form.querySelector('[name="nro_pedido"]').value,
                                    type: 'nro_pedido',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El pedido ya se encuentra registrado',
                            method: 'POST',
                            
                        }
                    }
                },
                descripcion: {
                    validators: {
                        notEmpty: {
                            message:'Descripcion es requerido'
                        },
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                destino: {
                    validators: {
                        notEmpty: {
                            message:'Destino es requerido'
                        },
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                nro_expediente: {
                    validators: {
                        notEmpty: {
                            message:'Nro Expediente es requerido'
                        },
                        stringLength: {
                            min: 6,
                        },
                    }
                },
            },
        }
        )
            .on('core.element.validated', function (e) {
                // console.log('core.element.validated');
                if (e.valid) {
                    const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                    if (groupEle) {
                        FormValidation.utils.classSet(groupEle, {
                            'has-success': false,
                        });
                    }
                    FormValidation.utils.classSet(e.element, {
                        'is-valid': false,
                    });
                }
                const iconPlugin = fv.getPlugin('icon');
                const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
                iconElement && (iconElement.style.display = 'none');
            })
            .on('core.validator.validated', function (e) {
                // console.log('core.validator.validated');
                if (!e.result.valid) {
                    const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                    messages.forEach((messageEle) => {
                        const validator = messageEle.getAttribute('data-validator');
                        messageEle.style.display = validator === e.validator ? 'block' : 'none';
                    });
                }
            })
            .on('core.form.valid', function () {
                console.log('core.form.valid');
                submit_formdata_with_ajax_form(fv);
            });
    // });


    $("#modal-movimiento").submit(function(){
        $(this).validate();
        
    });
};

function valores_por_defecto (){
     // SUCURSAL POR DEFECTO
     
     var action = $('#modal-movimiento input[name="action"]').val();    
     var sucursal_id = $('#modal-movimiento input[name="sucursal_id"]').val();    
     var fecha_actual = $('#modal-movimiento input[name="fecha_actual"]').val();    

     if (action =='add'){
        var sucursal = $('#modal-movimiento select[name="sucursal"]');    
        sucursal.val(sucursal_id).change();
     };
     

    // FECHA DATETIMEPICKER
    var fecha = $('#modal-movimiento input[name="fecha"]');
    (fecha.val() == '' ? fecha.val(fecha_actual) : 0)
    fecha.daterangepicker({
        language: 'auto',
        singleDatePicker: true,
        showDropdowns: true,
        minYear: 1901,
        // startDate: fecha.val(),
        locale: {
            format: 'DD/MM/YYYY',
        }
    });

 

};