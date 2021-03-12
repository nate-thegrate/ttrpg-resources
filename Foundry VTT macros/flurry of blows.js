async function main() {
    if (actor.data.data.resources.primary.value <= 0) {
        ui.notifications.warn("Out of Ki points!");
        return;
    }
    actor.data.data.resources.primary.value -= 1;
    const prof = actor.data.data.attributes.prof;
    const dex = actor.data.data.abilities.dex.mod;
    const dieSize = Math.ceil((actor.data.data.details.level +8)/6)*2;
    new Roll(`d20+${prof}+${dex}`).roll().toMessage({ flavor: "Attack 1", speaker });
    new Roll(`d20+${prof}+${dex}`).roll().toMessage({ flavor: "Attack 2", speaker });
    new Roll(`d${dieSize}+${dex}`).roll().toMessage({ flavor: "Damage 1", speaker });
    new Roll(`d${dieSize}+${dex}`).roll().toMessage({ flavor: "Damage 2", speaker });
}

main()
