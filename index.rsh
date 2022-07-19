'reach 0.1'

const shared = {
    see_token: Fun([Token], Null),
    getbal: Fun([], UInt)
}
export const main = Reach.App(() => {
    const User1 = Participant("User1", {
        getnftid: Token,
        minPrice: UInt
    })
    const User2 = Participant("User2", {
        ...shared
    })
    const User3 = Participant("User3", {
        ...shared
    })

    init()
    User1.only(() => {
        const NftId = declassify(interact.getnftid)
        const price = declassify(interact.minPrice)
    })
    User1.publish(NftId, price)
    const amt = 1
    commit()
    User1.pay([[amt, NftId]])
    commit()

    User2.only(() => {
        const user2bal = declassify(interact.getbal())
        const user2seetok = declassify(interact.see_token(NftId))
    })
    User2.publish(user2bal, user2seetok)
    commit()

    User3.only(() => {
        const user3bal = declassify(interact.getbal())
        const user3seetok = declassify(interact.see_token(NftId))
    })
    User3.publish(user3bal, user3seetok)
    const whitelisted_address = new Map(Address, UInt)
    if (user2bal > price) {
        whitelisted_address[User2] = user2bal
        transfer([[amt, NftId]]).to(User2)
    } else if (user3bal > price) {
        whitelisted_address[User3] = user3bal
        transfer([[amt, NftId]]).to(User3)
    } else {
        transfer([[amt, NftId]]).to(User1)
    }
    commit()
})
