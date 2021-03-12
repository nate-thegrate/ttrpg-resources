// Note: this macro only works with the module found at https://foundryvtt.com/packages/dae/

let dae_effect = async function() {
    const effect_name = "Sharpshooter";
    const effect = token.actor.effects.entries;
        for (let i = 0; i < effect.length; i++){
        let condition = effect[i].data.label;
        let status = effect[i].data.disabled;
        let effect_id = effect[i].data._id;
        if ((condition === effect_name) && (status === false)) {
            await token.actor.updateEmbeddedEntity("ActiveEffect", {"_id": effect_id, "disabled" : true});
            ui.notifications.info(effect_name + " is now inactive");
        }
        if ((condition === effect_name) && (status === true)){
            await token.actor.updateEmbeddedEntity("ActiveEffect", {"_id": effect_id, "disabled" : false});
            ui.notifications.info(effect_name + " is now active");
        }
    }
}

dae_effect();
