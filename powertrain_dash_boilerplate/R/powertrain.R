# AUTO GENERATED FILE - DO NOT EDIT

#' @export
powertrain <- function(id=NULL, label=NULL, value=NULL) {
    
    props <- list(id=id, label=label, value=value)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'Powertrain',
        namespace = 'powertrain_dash_boilerplate',
        propNames = c('id', 'label', 'value'),
        package = 'powertrainDashBoilerplate'
        )

    structure(component, class = c('dash_component', 'list'))
}
