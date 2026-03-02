scope1: "Scope.APP"{
component2: "Scope.APP"{
factory3: "📥 AsyncContainer"{
    shape: class
}

factory4: "🏭 Settings"{
    shape: class
    "SettingsProvider.get_settings()": ""
}

factory5: "🏭 AbstractDBConfig"{
    shape: class
    "SettingsProvider.get_db_config()": ""
    Settings
}

factory6: "🏭 DiscordSettings"{
    shape: class
    "SettingsProvider.get_discord_settings()": ""
    Settings
}

factory7: "🏭 RioSettings"{
    shape: class
    "SettingsProvider.get_rio_settings()": ""
    Settings
}

factory8: "🏭 AsyncEngine"{
    shape: class
    "DBProvider.get_engine()": ""
    AbstractDBConfig
}

factory9: "🏭 async_sessionmaker_AsyncSession_"{
    shape: class
    "DBProvider.get_sessionmaker()": ""
    AsyncEngine
}

factory10: "🏭 AsyncClient"{
    shape: class
    "HttpxProvider.get_async_client()": ""
}

factory11: "🏭 RaiderIOService"{
    shape: class
    "ServiceProvider.get_rio_service()": ""
    AsyncClient
    RioSettings
}

factory12: "🏭 CharacterUpdater"{
    shape: class
    "UpdateProvider.get_character_updater()": ""
    AsyncContainer
    RaiderIOService
}

}

}
scope1.component2.factory4 --> scope1.component2.factory5
scope1.component2.factory4 --> scope1.component2.factory6
scope1.component2.factory4 --> scope1.component2.factory7
scope1.component2.factory5 --> scope1.component2.factory8
scope1.component2.factory8 --> scope1.component2.factory9
scope1.component2.factory10 --> scope1.component2.factory11
scope1.component2.factory7 --> scope1.component2.factory11
scope1.component2.factory3 --> scope1.component2.factory12
scope1.component2.factory11 --> scope1.component2.factory12
scope13: "Scope.REQUEST"{
component14: "Scope.REQUEST"{
factory15: "📥 AsyncContainer"{
    shape: class
}

factory16: "🏭 AsyncSession"{
    shape: class
    "DBProvider.get_session()": ""
    async_sessionmaker_AsyncSession_
}

factory17: "🏭 UnitOfWork"{
    shape: class
    "UOWProvider.get_uow()": ""
    AsyncSession
}

factory18: "🏭 CharacterService"{
    shape: class
    "ServiceProvider.get_character_service()": ""
    UnitOfWork
}

factory19: "🏭 OwnerService"{
    shape: class
    "ServiceProvider.get_owner_service()": ""
    UnitOfWork
}

}

}
scope1.component2.factory9 --> scope13.component14.factory16
scope13.component14.factory16 --> scope13.component14.factory17
scope13.component14.factory17 --> scope13.component14.factory18
scope13.component14.factory17 --> scope13.component14.factory19
