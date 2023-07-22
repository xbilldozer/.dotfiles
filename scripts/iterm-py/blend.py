#!/usr/bin/env python3.7

import iterm2


async def main(connection):
    app = await iterm2.async_get_app(connection)

    async def get_profile_for_session(session_id):
        session = app.get_session_by_id(session_id)
        return await session.async_get_profile()

    @iterm2.RPC
    async def blend_more(session_id):
        profile = await get_profile_for_session(session_id)
        await profile.async_set_blend(min(1, profile.blend + 0.05))
    await blend_more.async_register(connection)

    @iterm2.RPC
    async def blend_less(session_id):
        profile = await get_profile_for_session(session_id)
        await profile.async_set_blend(max(0, profile.blend - 0.05))
    await blend_less.async_register(connection)

    @iterm2.RPC
    async def blend_reset(session_id):
        profile = await get_profile_for_session(session_id)
        await profile.async_set_blend(0.20)
    await blend_reset.async_register(connection)

iterm2.run_forever(main)

