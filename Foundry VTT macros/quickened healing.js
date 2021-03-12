async function main() {
    if(!character) {
        ui.notifications.error("Couldn't locate character");
        return;
    }
    let feature = character.data.data.resources.primary;
    if(feature.value <= 1) {
        ui.notifications.warn("Not enough Ki points!");
        return;
    }

    const prof = character.data.data.attributes.prof;
    const dieSize = Math.ceil((actor.data.data.details.level +8)/6)*2;

    await character.update({"data.resources.primary.value": feature.value - 2});
    let roll = new Roll(`d${dieSize}+${prof}`).roll();
    roll.toMessage({ flavor: "Quickened Healing", speaker });
    token.actor.applyDamage(-roll.total);
}
main();
