"""Objects representing a database and database objects for storing health summary data from a Garmin device."""

__author__ = "Tom Goetz"
__copyright__ = "Copyright Tom Goetz"
__license__ = "GPL"

import logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, DateTime

import HealthDB
import utilities


logger = logging.getLogger(__name__)


class GarminSummaryDB(utilities.DB):
    """Object representing a database for storing health summary data from a Garmin device."""

    Base = declarative_base()

    db_tables = []
    db_name = 'garmin_summary'
    db_version = 7

    class _DbVersion(Base, utilities.DbVersionObject):
        """Stores version information for this databse and it's tables."""


class Summary(GarminSummaryDB.Base, utilities.KeyValueObject):
    """A table holding statistics about health data as key-value pairs."""

    __tablename__ = 'summary'

    db = GarminSummaryDB
    table_version = 1


class YearsSummary(GarminSummaryDB.Base, HealthDB.SummaryBase):
    """A table holding summarized data with one row per year."""

    __tablename__ = 'years_summary'

    db = GarminSummaryDB
    table_version = 4
    view_version = HealthDB.SummaryBase.view_version

    first_day = Column(Date, primary_key=True)

    @classmethod
    def create_view(cls, db):
        """Create the default database view for the table."""
        cls.create_years_view(db)


class MonthsSummary(GarminSummaryDB.Base, HealthDB.SummaryBase):
    """A table holding summarized data with one row per month."""

    __tablename__ = 'months_summary'

    db = GarminSummaryDB
    table_version = 4
    view_version = HealthDB.SummaryBase.view_version

    first_day = Column(Date, primary_key=True)

    @classmethod
    def create_view(cls, db):
        """Create the default database view for the table."""
        cls.create_months_view(db)


class WeeksSummary(GarminSummaryDB.Base, HealthDB.SummaryBase):
    """A table holding summarizzed data with one row per week."""

    __tablename__ = 'weeks_summary'

    db = GarminSummaryDB
    table_version = 4
    view_version = HealthDB.SummaryBase.view_version

    first_day = Column(Date, primary_key=True)

    @classmethod
    def create_view(cls, db):
        """Create the default database view for the table."""
        cls.create_weeks_view(db)


class DaysSummary(GarminSummaryDB.Base, HealthDB.SummaryBase):
    """A table holding summarizzed data with one row per day."""

    __tablename__ = 'days_summary'

    db = GarminSummaryDB
    table_version = 4
    view_version = HealthDB.SummaryBase.view_version

    day = Column(Date, primary_key=True)

    @classmethod
    def create_view(cls, db):
        """Create the default database view for the table."""
        cls.create_days_view(db)


class IntensityHR(GarminSummaryDB.Base, utilities.DBObject):
    """Monitoring heart rate values that fall within a intensity period."""

    __tablename__ = 'intensity_hr'

    db = GarminSummaryDB
    table_version = 1

    timestamp = Column(DateTime, primary_key=True)
    intensity = Column(Integer, nullable=False)
    heart_rate = Column(Integer, nullable=False)

    @classmethod
    def get_stats(cls, session, start_ts, end_ts):
        """Return a dictionary of aggregate statistics for the given time period."""
        return {
            'inactive_hr_avg' : cls.s_get_col_avg_for_value(session, cls.heart_rate, cls.intensity, 0, start_ts, end_ts, True),
            'inactive_hr_min' : cls.s_get_col_min_for_value(session, cls.heart_rate, cls.intensity, 0, start_ts, end_ts, True),
            'inactive_hr_max' : cls.s_get_col_max_for_value(session, cls.heart_rate, cls.intensity, 0, start_ts, end_ts, True),
        }
