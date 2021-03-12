async function main() {
    if(!character) {
        ui.notifications.error("Couldn't locate character");
        return;
    }
    let feature = character.items.find(i=>i.name===`Second Wind`);
    if(!feature || feature.data.data.uses.value === 0) {
        ui.notifications.warn("Out of Second Wind uses");
        return;
    }
    await feature.update({"data.uses.value": feature.data.data.uses.value - 1});
    let roll = new Roll(`1d10 + ${parseInt(actor.items.find(i => i.name == "Fighter").data.data.levels)}`).roll();
    roll.toMessage({ flavor: "Second Wind", speaker });
    await token.actor.applyDamage(-roll.total);
}
main();
