main()

async function main() {
    let targets = Array.from(game.user.targets)
    if (targets.length == 0) {
        ui.notifications.warn("Please target a token");
        return;
    }

    Hooks.once('renderChatMessage', (chatItem, html) => {
        for (let i = 0; i < game.user.targets.size; i++) {
            targets[i].actor.applyDamage(html[0].lastElementChild.getElementsByClassName("dice-total")[0].innerText);
        }
    })
}
