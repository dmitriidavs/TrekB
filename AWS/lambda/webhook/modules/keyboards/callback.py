from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..database.logic import get_supported_networks


wallet_address_cd = CallbackData('list_networks', 'network_id', 'network_name', 'wallet_address')


def create_cd_bc(network_id: int, network_name: str, wallet_address: str = '_wallet_address_err') -> str:
    return wallet_address_cd.new(network_id=network_id, network_name=network_name, wallet_address=wallet_address)


async def bc_networks_keyboard() -> InlineKeyboardMarkup:
    """Create supported blockchain networks inline keyboard"""

    markup = InlineKeyboardMarkup(row_width=2)

    # request supported networks data from olap
    bc_networks = await get_supported_networks()

    # create a button for each network and add it to markup
    for network in bc_networks:
        # create callback data
        cllbck_data = create_cd_bc(network_id=network[0],
                                   network_name=network[1])
        # add button
        markup.add(
            InlineKeyboardButton(text=network[1],
                                 callback_data=cllbck_data)
        )

    return markup
