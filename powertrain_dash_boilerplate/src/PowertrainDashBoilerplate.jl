
module PowertrainDashBoilerplate
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "0.0.1"

include("jl/powertrain.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "powertrain_dash_boilerplate",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "powertrain_dash_boilerplate.min.js",
    external_url = "https://unpkg.com/powertrain_dash_boilerplate@0.0.1/powertrain_dash_boilerplate/powertrain_dash_boilerplate.min.js",
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "powertrain_dash_boilerplate.min.js.map",
    external_url = "https://unpkg.com/powertrain_dash_boilerplate@0.0.1/powertrain_dash_boilerplate/powertrain_dash_boilerplate.min.js.map",
    dynamic = true,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end
