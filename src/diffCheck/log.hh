#pragma once

#include <loguru.hpp>

namespace diffCheck
{
    class Log
    {
    public:
        Log() { Init(); }
        ~Log() { Shutdown(); }

    private:
        void Init();
        void Shutdown();
    };
}

#ifndef SILENT_LOGGING
    #define DIFFCHECK_INFO(message) LOG_F(INFO, message)
    #define DIFFCHECK_WARN(message) LOG_F(WARNING, message)
    #define DIFFCHECK_ERROR(message) LOG_F(ERROR, message)
    #define DIFFCHECK_FATAL(message) LOG_F(FATAL, message)
#else
    #define DIFFCHECK_INFO
    #define DIFFCHECK_WARN
    #define DIFFCHECK_ERROR
    #define DIFFCHECK_FATAL
#endif